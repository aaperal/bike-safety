// store data so we don't keep loading json files
var stations;
var coordinates;

/* 
 * Gets data from loaded json files.
 * Inputs:
 * stats - json file that has number of visits per station for 
 * our given time frame (2017-2019). Derived from dataframe where
 * columns are station names, rows are specific date/time combination
 * Row values are number of visits during that given hour. Example below.
 *
 * station_names ->      station0 | station1 | station2 | ... | stationx
 * datehour 
 * (yyyy-mm-dd hh:mm:ss)	
 *	
 * 2017-06-28 00:00:00	  #visit0 | #visit1  | #visit2  | ... | #visitx
 * 2017-06-28 01:00:00    
 * ...
 * 2019-03-31 23:00:00
 *
 * coords - json file that lists name of station and their respective 
 * latitude/longitude coordinates.
 *
 * date - date string within range [2017-06-28 00:00:00, 2019-03-31 23:00:00]
 * 
 * Returns: 
 * station_array - an array of arrays that contain 
 * [latitude, longitude, num_visits] for each given station name.
 * 
 */
function getData(stats, coords, date) {
	stations = stats;
	coordinates = coords;
	var station_array = []

	// iterates over station names
	for (station in stations) {
		
		// get latitude and longitude corresponding to station
		var coords = coordinates[station]
		// the first case is the default loading
		// otherwise get the corresponding number of visits for a given date+time
		if (!date) {
			station_array.push([coords[0], coords[1], stations[station]["2019-03-30 19:00:00"]]);
		} else {
			station_array.push([coords[0], coords[1], stations[station][date]]);
		}
	}
	return station_array
}
// Want to save the heat layer so we can update + redraw it
var heat;
var map;
// generates initial heatmap
function generateMap(circles) {
		map = L.map('map', {
			zoomSnap: 0.1,
			zoomDelta: 0.5
		}).setView([37.775395,-122.447601], 12);
        //mapLink = 
        //    '<a href="http://openstreetmap.org">OpenStreetMap</a>';
        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    		maxZoom: 18,
    		id: 'mapbox.streets',
    		accessToken: 'pk.eyJ1IjoiYXBlcmFsb3IiLCJhIjoiY2p2cTloczE0Mmh1cjRhb2pjMm8zanR1byJ9.ys1LliIhGNDHIioORQq9NA'
		}).addTo(map);
        
        heat = L.heatLayer(circles,{
            radius: 15,
            blur: 15, 
            maxZoom: 17,
        }).addTo(map);

    return heat;

}

// Updates heat layer with corresponding date data
function updateData(date) {

	// gets updated data with new date
	var circles = getData(stations, coordinates, date);

	// update and redraw heat layer
	heat.setLatLngs(circles);
	heat.redraw();

}


// transforms the severity index into its corresponding string
function severityToString(num) {
	switch (num) {
  		case 1:
    		return "Fatal";
  		case 2:
    		return "Injury (Severe)";
  		case 3:
    		return "Injury (Other Visible)";
  		case 4:
  			return "Injury (Complaint of Pain)";
  		case 0:
  			return "PDO";
	}
}

/*
 * 
 * Extracts relevant accident information from json format.
 *
 */
function getAccidentData(accident) {
	// getting all the relevant info
	var severity = severityToString(accident['severity']);
	var injured = accident['num_injured'];
	var killed = accident['num_killed'];
	var date = accident['year'] + "-" + accident['month'] + "-" + accident['day'];
	// Will probably not yet use time or day of week
	var time = accident['time']
	var day_of_week = accident['day_of_week']
			
	// string to display on hover
	var display_string = ("Date: "+ date + "\n" + 
	"Severity: " + severity + "\n" + "Number Injured: " + injured + "\n" + 
	"Number killed: " + killed);
			
	// coordinates for accident
	var lat = accident['coordinates'][0];
	var longitude = accident['coordinates'][1];	

	return [lat, longitude, display_string];
}

var tooltips;
var accidents;
var month;
var year;
// Adds accident data depending on selected date
function addAccidents(accs, m, y) {
	tooltips = [];
	month = m;
	year = y;
	accidents = accs;
	for (index in accidents) {
		var accident = accidents[index];
		if (accident['month'] == month && accident['year'] == year) {
			
			// accident information (latitude, longitude, display string)
			var info = getAccidentData(accident);

			// custom picture for icon
			var crashIcon = L.icon({
   				iconUrl: '/img/accident.png',
   				iconSize: [24,24],
    			//iconSize: [38, 95],
    			//iconAnchor: [24, 24],
    			//popupAnchor: [-3, -76],
			});
			// tooltip
			var tool = L.marker([info[0], info[1]], {
				title: info[2], // text display on hover
				alt: info[2], // for accessibility
				riseOnHover: true, // brings icon to front on mouse hover
				icon: crashIcon // our custom crash icon
			}).addTo(map);
		
			tooltips.push(tool);
		}
	}
	document.getElementById("accidentCount").innerHTML = "Accident count for the month: " + tooltips.length;
}

// updates accident tool tips when date information is changed
function updateToolTip(m, y) {
	//console.log("month: " + month + " year: " + year);
	//console.log("m : " + m + " y: " + y);
	if (month != m || year != y) {
		month = m; year = y;
		for (tool in tooltips) {
			map.removeLayer(tooltips[tool]);
		}
		tooltips = [];
		addAccidents(accidents, month, year);
	}
}
