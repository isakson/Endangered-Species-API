#!/usr/bin/env python3
'''
    converter.py
    Cayden Ehrlich and Irene Sakson, 27 April 2017
    
'''

import sys
import re
import csv

def load_from_species_csv_file(csv_file_name):
    
    csv_file = open(csv_file_name)
    reader = csv.reader(csv_file)

    species_list = []
    species_groups = {}
    fls_values = {"endangered": 0, "threatened": 1, "experimental population, non-essential": 2, "similarity of appearance to a threatened taxon": 3}
    location_values = {"wherever found": 0}
    species_fls_location = []

    for row in reader:
        assert len(row) == 7
        species_id = len(species_list)
        
        group_val = row[3].lower()    
        fls_val = row[4].lower()
        loc_val = row[6].lower()
        
        if group_val in species_groups:
            group_id = species_groups[group_val]
        else:
            group_id = len(species_groups)
            species_groups[group_val] = group_id
            
            
        if species_id == 0 or species_list[species_id - 1]['scientific_name'] != row[0]:
            species = {'species_id': species_id, 'scientific_name': row[0], 'common_name': row[1], 'species_group': group_id}
            species_list.append(species)
        elif species_id !=0 and species_list[species_id - 1]['scientific_name'] == row[0]:
            #To make the species_id correspond with the entry for this species
            species_id = species_list[species_id - 1]['species_id']
            
    
        fls_val_id = fls_values[fls_val]
        
        if loc_val in location_values:
            location_id = location_values[loc_val]
        else:
            location_id = len(location_values)
            location_values[loc_val] = location_id
        
        
        
        species_fls_location.append({'species_id': species_id, 'fls_val_id': fls_val_id, 'location_id': location_id})
        
    csv_file.close()
    return (species_list, species_groups, fls_values, location_values, species_fls_location)

def save_species_list_table(species_list, csv_file_name):
    ''' Save the books in CSV form, with each row containing
        (id, title, publication year). '''
    output_file = open(csv_file_name, 'w')
    writer = csv.writer(output_file)
    for species in species_list:
        species_row = [species['species_id'], species['scientific_name'], species['common_name'], species['species_group']]
        writer.writerow(species_row)
    output_file.close()
    
def save_species_groups_table(species_groups, csv_file_name):
    ''' Save the books in CSV form, with each row containing
        (id, last name, first name, birth year, death year), where
        death year can be NULL. '''
    output_file = open(csv_file_name, 'w')
    writer = csv.writer(output_file)
    for key in species_groups:
        species_group_row = [species_groups[key], key]
        writer.writerow(species_group_row)
    output_file.close()

def save_fls_values_table(fls_values, csv_file_name):
    ''' Save the books in CSV form, with each row containing
        (id, last name, first name, birth year, death year), where
        death year can be NULL. '''
    output_file = open(csv_file_name, 'w')
    writer = csv.writer(output_file)
    for key in fls_values:
        fls_values_row = [fls_values[key], key]
        writer.writerow(fls_values_row)
    output_file.close()
    
def save_location_values_table(location_values, csv_file_name):
    ''' Save the books in CSV form, with each row containing
        (id, last name, first name, birth year, death year), where
        death year can be NULL. '''
    output_file = open(csv_file_name, 'w')
    writer = csv.writer(output_file)
    for key in location_values:
        location_values_row = [location_values[key], key]
        writer.writerow(location_values_row)
    output_file.close()

def save_linking_table(species_fls_location, csv_file_name):
    ''' Save the books in CSV form, with each row containing
        (book id, author id). '''
    output_file = open(csv_file_name, 'w')
    writer = csv.writer(output_file)
    for entry in species_fls_location:
        species_fls_location_row = [entry['species_id'], entry['fls_val_id'], entry['location_id']]
        writer.writerow(species_fls_location_row)
    output_file.close()

if __name__ == '__main__':
    species_list, species_groups, fls_values, location_values, species_fls_location = load_from_species_csv_file('speciesCSV.csv')

    save_species_list_table(species_list, 'species_list.csv')
    save_species_groups_table(species_groups, 'species_groups.csv')
    save_fls_values_table(fls_values, 'fls_values.csv')
    save_location_values_table(location_values, 'location_values.csv')
    save_linking_table(species_fls_location, 'species_fls_location.csv')

