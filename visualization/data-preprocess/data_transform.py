import csv
import pandas as pd
import json

'''
Want our json file to look like:

{"stations":[
{"station_name0": [
{"datehour0":0.0},
{"datehour1":1.1} ]},
{"station_name1": [
{"datehour0":0.0},
{"datehour1":1.1} ]}
]}
'''


def csv_to_json(csv_name):
	station_data = pd.DataFrame(pd.read_csv(csv_name, index_col = 0))

	stations = {}

	# this should return a list of the columns, over which we will iterate
	# columns = list(station_data)
	times = []
	# iterating over the rows 
	for index, row in station_data.iterrows():
		#print(row[0])
		#print("barrier")
		#print(index)
		datehour = ''
		for item in row.iteritems():
			# we get the corresponding datehour
			print(item[0])
			if item[0] == 'datehour':
				datehour = str(item[1])
			# check if the station already in our dictionary of station names
			elif item[0] not in stations:
				stations[item[0]] = {datehour:item[1]}
			else:
				stations.get(item[0])[datehour] = item[1]

	return stations

def make_collision_json():
	collision_data = pd.DataFrame(pd.read_csv('collision_data.csv'))

	collisions = {}
	#index is index on the left hand side
	#row[0] is index
	#row[1] is primary rd... and so on
	for index, row in collision_data.iterrows():
		collisions[index] = {
			"year": row[1],
			"severity": row[4],
			"time": row[5],
			"day_of_week": row[8],
			"coordinates": [row[12],row[13]],
			"month": row[20],
			"day": row[21],
			"num_injured": row[14],
			"num_killed": row[15]
		}
	with open('collision_data.json', 'w') as fp:
		json.dump(collisions, fp)
	print(collisions)

#make_collision_json()
#stations = csv_to_json('predictions_top25_stations.csv')
#stations = csv_to_json('station_data.csv')
with open('bike_predictions.json', 'w') as fp:
    json.dump(stats, fp)
#print(stations)