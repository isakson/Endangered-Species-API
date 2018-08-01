#!/usr/bin/env python3
'''
    psycopg2-sample.py
    Cayden Ehrlich and Irene Sakson
    May 2, 2018
'''
import psycopg2
import sys
import flask
import json

from config import password
from config import database
from config import user

app = flask.Flask(__name__)

@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def hello():
    return 'Welcome to the endangered species API.'

@app.route('/species/')
def get_all_species():
    ''' Returns the list of all species. Sorted by scientific name by default, but can be sorted by common name, fls, location, or species group.'''
    species_list = []
   
    query = '''SELECT t.species_id, c, s, g, fls
        FROM fls_values,
        (SELECT species.id as species_id, common_name as c, scientific_name as s, group_val as g, min(fls_values.id) as m
        FROM species, species_group, location_values, fls_values, species_fls_location
        WHERE species.id = species_fls_location.species_id
            AND fls_values.id = species_fls_location.fls_id
            AND location_values.id = species_fls_location.location_id
            AND species.species_group = species_group.id
        GROUP BY species.id, common_name, scientific_name, group_val) as t
        WHERE t.m = fls_values.id
        ORDER BY '''

    sort_argument = flask.request.args.get('sort')
    if sort_argument == 'common_name':
        query += 'c, s'
    elif sort_argument == 'fls':
        query += 'fls, s'
    elif sort_argument == 'species_group':
        query += 'g, s'
    else:
        query += 's' 
    connection = get_connection()

    try:     
        cursor = select_query_results(connection, query)
    except Exception as e:
        print(e)
        exit()

    # Iterate over its rows to print the results.
    try:
        for row in cursor:
            species = {'id': row[0], 'scientific_name': row[2], 'common_name': row[1], 'species_group': row[3], 'fls_value': row[4]}
            species_list.append(species)
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(species_list)
    connection.close()
    
@app.route('/species/id/<species_id>')
def get_species_by_id(species_id):
    ''' Returns information on the species with the given id. Given an empty list if there does not exist any species with that id.
    If there are multiple entries for the species, they are sorted by scientific name by default, but can be sorted by common name, fls, location, or species group.'''
    species = []
    
    query = '''SELECT species.id, species.common_name, species.scientific_name, species_group.group_val, location_values.location, fls_values.fls
        FROM species, species_group, fls_values, species_fls_location, location_values
        WHERE species.id = {0}
            AND species.species_group = species_group.id
            AND species.id = species_fls_location.species_id
            AND fls_values.id = species_fls_location.fls_id
            AND location_values.id = species_fls_location.location_id
        ORDER BY '''.format(species_id)
    
    sort_argument = flask.request.args.get('sort')
    query += get_sort_order(sort_argument)
    
    connection = get_connection()

    try:
        cursor = select_query_results(connection, query)
    except Exception as e:
        print(e)
        exit()

    # Iterate over its rows to print the results.
    try:
        rows = cursor.fetchall()
        speciesData = {'id': rows[0][0], 'scientific_name': rows[0][2], 'common_name': rows[0][1], 'species_group': rows[0][3]}
        species.append(speciesData)
        for row in rows:
            locationData = {'location': row[4], 'fls_value': row[5]}
            species.append(locationData)
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(species)
    connection.close()

@app.route('/species/search/<search_string>')
def get_species_by_search_string(search_string):
    ''' Returns information on all species that match the search string. Given an empty list if there does not exist any species that match the search string. Sorted by scientific name by default, but can be sorted by common name, fls, location, or species group.'''
    species_list = []
    search_string = search_string.lower()
    
    query = '''SELECT species.id, species.common_name, species.scientific_name, species_group.group_val, location_values.location, fls_values.fls
        FROM species, species_group, fls_values, species_fls_location, location_values
        WHERE species.species_group = species_group.id
            AND species.id = species_fls_location.species_id
            AND fls_values.id = species_fls_location.fls_id
            AND location_values.id = species_fls_location.location_id
            AND (LOWER(species.common_name) LIKE '%{0}%' OR LOWER(species.scientific_name) LIKE '%{0}%')
        ORDER BY '''.format(search_string)
    
    sort_argument = flask.request.args.get('sort')
    query += get_sort_order(sort_argument)
    
    connection = get_connection()

    try:
        cursor = select_query_results(connection, query)
    except Exception as e:
        print(e)
        exit()

    # Iterate over its rows to print the results.
    try:
        for row in cursor:
            species = {'id': row[0], 'scientific_name': row[2], 'common_name': row[1], 'species_group': row[3],'location': row[4], 'fls_value': row[5]}
            species_list.append(species)
    except Exception as e:
        print(e, file=sys.stderr)
        
    return json.dumps(species_list)
    connection.close()
    
    
@app.route('/fls/<fls>')
def get_species_by_fls(fls):
    ''' Returns information on all species with the given fls value. Given an empty list if there does not exist any species with that fls value. Sorted by scientific name by default, but can be sorted by common name, fls, location, or species group.'''
    species_list = []
    fls = fls.lower()
    
    query = '''SELECT species.id, species.common_name, species.scientific_name, species_group.group_val, location_values.location, fls_values.fls
        FROM species, species_group, fls_values, species_fls_location, location_values
        WHERE species.species_group = species_group.id
            AND species.id = species_fls_location.species_id
            AND fls_values.id = species_fls_location.fls_id
            AND fls_values.fls LIKE '{0}%'
            AND location_values.id = species_fls_location.location_id
        ORDER BY '''.format(fls)
    
    sort_argument = flask.request.args.get('sort')
    query += get_sort_order(sort_argument)
    
    connection = get_connection()

    try:
        cursor = select_query_results(connection, query)
    except Exception as e:
        print(e)
        exit()

    # Iterate over its rows to print the results.
    try:
        for row in cursor:
            species = {'id': row[0], 'scientific_name': row[2], 'common_name': row[1], 'species_group': row[3],'location': row[4], 'fls_value': row[5]}
            species_list.append(species)
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(species_list)
    connection.close()
    
@app.route('/species_group/<species_group>')
def get_species_by_group(species_group):
    ''' Returns information on all species with the given species group. Given an empty list if there does not exist any species with that species group. Sorted by scientific name by default, but can be sorted by common name, fls, location, or species group.'''
    species_list = []
    species_group = species_group.lower()
    
    query = '''SELECT species.id, species.common_name, species.scientific_name, species_group.group_val, location_values.location, fls_values.fls
        FROM species, species_group, fls_values, species_fls_location, location_values
        WHERE species.species_group = species_group.id
            AND species.id = species_fls_location.species_id
            AND fls_values.id = species_fls_location.fls_id
            AND species_group.group_val LIKE '{0}%'
            AND location_values.id = species_fls_location.location_id
        ORDER BY '''.format(species_group)
    
    sort_argument = flask.request.args.get('sort')
    query += get_sort_order(sort_argument)
    
    connection = get_connection()

    try:
        cursor = select_query_results(connection, query)
    except Exception as e:
        print(e)
        exit()

    # Iterate over its rows to print the results.
    try:
        for row in cursor:
            species = {'id': row[0], 'scientific_name': row[2], 'common_name': row[1], 'species_group': row[3],'location': row[4], 'fls_value': row[5]}
            species_list.append(species)
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(species_list)
    connection.close()

    
'''Connects to the database.'''
def get_connection():
    connection = None
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e, file=sys.stderr)
    return connection

'''Queries the database.'''
def select_query_results(connection, query, parameters=None):
    cursor = connection.cursor()
    if parameters is not None:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    return cursor

'''Determines what to add to the query (after 'ORDER BY ') to sort the results.'''
def get_sort_order(sort_argument):
    if sort_argument == 'common_name':
        return 'species.common_name, species.scientific_name'
    elif sort_argument == 'fls':
        return 'fls_values.id, species.scientific_name'
    elif sort_argument == 'species_group':
        return 'species_group.group_val, species.scientific_name'
    elif sort_argument == 'location':
        return 'location_values.location, species.scientific_name'
    else:
        return 'species.scientific_name'

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
        exit()
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)
