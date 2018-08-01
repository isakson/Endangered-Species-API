initialize();

function initialize() {
        var element = document.getElementById('all_species_button');
            if (element) {
                element.onclick = onAllSpeciesButtonClicked();
            }
}

function getBaseURL() {
        var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + api_port;
            return baseURL;
}

function onAllSpeciesButtonClicked() {
    var url = getBaseURL() + '/species/';

    // Send the request to the Endangered Species API /species/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from JSON string into a Javascript object.
    .then((response) => response.json())

    // Use this list to build an HTML table displaying species information.
    .then(function(speciesList) {

        var speciesNames ='';
        var speciesGroup = '';

        tableBody = '';
        for (var k = 0; k < speciesList.length; k++) {
            linkText = 'getSpecies(12)';
            tableBody += '<tr>';

            tableBody += '<td><a href="javascript:getSpecies(' + speciesList[k]['id'] + ")\">" + speciesList[k]['scientific_name'] + '</a></td>';

            tableBody += '<td>' + speciesList[k]['common_name'] + '</td>';
            tableBody += '<td>' + speciesList[k]['species_group'] + '</td>';
            tableBody += '<td>' + speciesList[k]['fls_value'] + '</td>';

            tableBody += '</tr>';
        }

        // Put the table body inside the table that's already on the page.
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = '<tr><th id="scientific_name">Scientific Name</th><th id="common_name">Common Name</th><th id="species_group">Species Group</th><th id="fls">Federal Listing Status</th></tr>' + tableBody;
        }
        var speciesNamesElement = document.getElementById('species_names');
        if (speciesNamesElement) {
            speciesNamesElement.innerHTML = speciesNames;
        }
        
        var speciesGroupElement = document.getElementById('species_group');
        if (speciesGroupElement) {
            speciesGroupElement.innerHTML = speciesGroup;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function getSpecies(speciesID) {
    var url = getBaseURL() + '/species/id/' + speciesID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(speciesDetails) {
        var speciesNames = speciesDetails[0]['scientific_name'] + ': ' + speciesDetails[0]['common_name'];
        var speciesGroup = speciesDetails[0]['species_group'];
        
        tableBody = '';
        for (var k = 1; k < speciesList.length; k++) {
            tableBody += '<tr>';
            tableBody += '<td>' + speciesList[k]['fls'] + '</td>';
            tableBody += '<td>' + speciesList[k]['location'] + '</td>';
            tableBody += '</tr>';
        }
        var speciesNamesElement = document.getElementById('species_names');
        if (speciesNamesElement) {
            speciesNamesElement.innerHTML = speciesDetails;
        }
        
        var speciesGroupElement = document.getElementById('species_group');
        if (speciesGroupElement) {
            speciesGroupElement.innerHTML = speciesGroup;
        }
        
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = '<tr><th id="fls">Federal Listing Status</th><th id="location">Location</th></tr>' + tableBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onFLSButtonClicked(fls_value) {
    var url = getBaseURL() + '/fls/' + fls_value;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(speciesList) {

        var speciesNames ='';
        var speciesGroup = '';

        tableBody = '';
        for (var k = 0; k < speciesList.length; k++) {
            tableBody += '<tr>';

            tableBody += '<td><a href="javascript:getSpecies(' + speciesList[k]['id'] + ')">' + speciesList[k]['scientific_name'] + '</a></td>';

            tableBody += '<td>' + speciesList[k]['common_name'] + '</td>';
            tableBody += '<td>' + speciesList[k]['species_group'] + '</td>';
            tableBody += '<td>' + speciesList[k]['location'] + '</td>';
            tableBody += '<td>' + speciesList[k]['fls_value'] + '</td>';

            tableBody += '</tr>';
        }

        // Put the table body inside the table that's already on the page.
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = '<tr><th id="scientific_name">Scientific Name</th><th id="common_name">Common Name</th><th id="species_group">Species Group</th><th id="location">Location</th><th id="fls">Federal Listing Status</th></tr>' + tableBody;
        }
        var speciesNamesElement = document.getElementById('species_names');
        if (speciesNamesElement) {
            speciesNamesElement.innerHTML = speciesNames;
        }
        
        var speciesGroupElement = document.getElementById('species_group');
        if (speciesGroupElement) {
            speciesGroupElement.innerHTML = speciesGroup;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function onGroupButtonClicked(species_group) {
    var url = getBaseURL() + '/species_group/' + species_group;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(speciesList) {
        
        var speciesNames ='';
        var speciesGroup = '';

        tableBody = '';
        for (var k = 0; k < speciesList.length; k++) {
            tableBody += '<tr>';

            tableBody += '<td><a href="javascript:getSpecies(' + speciesList[k]['id'] + ')">' + speciesList[k]['scientific_name'] + '</a></td>';

            tableBody += '<td>' + speciesList[k]['common_name'] + '</td>';
            tableBody += '<td>' + speciesList[k]['species_group'] + '</td>';
            tableBody += '<td>' + speciesList[k]['location'] + '</td>';
            tableBody += '<td>' + speciesList[k]['fls_value'] + '</td>';

            tableBody += '</tr>';
        }

        // Put the table body we just built inside the table that's already on the page.
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = '<tr><th id="scientific_name">Scientific Name</th><th id="common_name">Common Name</th><th id="species_group">Species Group</th><th id="location">Location</th><th id="fls">Federal Listing Status</th></tr>' + tableBody;
        }
        var speciesNamesElement = document.getElementById('species_names');
        if (speciesNamesElement) {
            speciesNamesElement.innerHTML = speciesNames;
        }
        
        var speciesGroupElement = document.getElementById('species_group');
        if (speciesGroupElement) {
            speciesGroupElement.innerHTML = speciesGroup;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}


function onSearchButtonClicked() {
    search_string = document.getElementById('search').value;
    var url = getBaseURL() + '/species/search/' + search_string;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(speciesList) {
        
        var speciesNames ='';
        var speciesGroup = '';
        
        tableBody = '';
        for (var k = 0; k < speciesList.length; k++) {
            tableBody += '<tr>';

            tableBody += '<td><a href="javascript:getSpecies(' + speciesList[k]['id'] + ')">' + speciesList[k]['scientific_name'] + '</a></td>';

            tableBody += '<td>' + speciesList[k]['common_name'] + '</td>';
            tableBody += '<td>' + speciesList[k]['species_group'] + '</td>';
            tableBody += '<td>' + speciesList[k]['location'] + '</td>';
            tableBody += '<td>' + speciesList[k]['fls_value'] + '</td>';

            tableBody += '</tr>';
        }

        // Put the table body we just built inside the table that's already on the page.
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = '<tr><th id="scientific_name">Scientific Name</th><th id="common_name">Common Name</th><th id="species_group">Species Group</th><th id="location">Location</th><th id="fls">Federal Listing Status</th></tr>' + tableBody;
        }
        var speciesNamesElement = document.getElementById('species_names');
        if (speciesNamesElement) {
            speciesNamesElement.innerHTML = speciesNames;
        }
        
        var speciesGroupElement = document.getElementById('species_group');
        if (speciesGroupElement) {
            speciesGroupElement.innerHTML = speciesGroup;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}
