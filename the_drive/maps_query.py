# maps_query.py
# 
# Script to query Google Maps using the distance matrix API call to obtain duration in
# traffic between a set of waypoints. 
# 
# Waypoints are logged to durations_log.csv for processing by another script. 


import requests
import csv
import json
from datetime import datetime
from datetime import date


api_key = "ENTER YOUR GOOGLE MAPS API KEY HERE"
waypoints = []


def get_info(orig_string, dest_string):
	response = ""
	url = "https://maps.googleapis.com/maps/api/distancematrix/json\
?origins="+orig_string +\
"&destinations="+dest_string+\
"&departure_time=now\
&key="+api_key\

	payload = {}
	headers = {}

	response = requests.request("GET", url, headers=headers, data=payload)
	#print(response.text)


	origin = orig_lat + ',' + orig_lon
	destination = dest_lat + ',' + dest_lon

	origin_address = str(response.json()['origin_addresses'])[2:-2]
	destination_address = str(response.json()['destination_addresses'])[2:-2]

	# Get distance in meters
	distance = response.json()['rows'][0]['elements'][0]['distance']['value']
	# Get normal trip duration in seconds
	duration = response.json()['rows'][0]['elements'][0]['duration']['value']
	# Get actual trip duration with traffic in seconds
	duration_in_traffic = response.json()['rows'][0]['elements'][0]['duration_in_traffic']['value']
	
	# Write to files
	traffic_duration_data_file.write(str(duration_in_traffic) + ",")
	ideal_duration_data_file.write(str(duration) + ",")
	distance_data_file.write(str(distance) + ",")


## MAIN LOOP

# READ IN WAYPOINTS FROM WAYPOINTS.CSV
#print("Started...")
# Get date
today = date.today()
#print("Today's date:", today)
# Get time in MST 24-hour format
now = datetime.now()
current_time = now.strftime("%H:%M")

print("Started", today, current_time)
#print("Reading in waypoints...")
try:
	with open('/home/pi/the_drive/waypoints.csv', newline ='') as csvfile:
		waypoint_reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		for row in waypoint_reader:
			lat = row[0][1:]
			lon = row[1][:-1]
			waypoints.append([str(lat), str(lon)])
except:
	print("Exception while reading in waypoints")

#print("Waypoints ingested")

#print("Opening data files...")
try:
	traffic_duration_data_file = open("/home/pi/the_drive/traffic_duration_data.csv", "a")
	ideal_duration_data_file = open("/home/pi/the_drive/ideal_duration_data.csv", "a")
	distance_data_file = open("/home/pi/the_drive/distance_data.csv", "a")
except:
	print("Exception while opening data files")

i = 0

#print("Writing date and time...")
traffic_duration_data_file.write(str(today) + "," + str(current_time) + ",")
ideal_duration_data_file.write(str(today) + "," + str(current_time) + ",")
distance_data_file.write(str(today) + "," + str(current_time) + ",")

#print("Current Time =", current_time)
#print("Querying for durations data...")

#print(str(int(len(waypoints)/2) - 1))

for x in range((int(len(waypoints)/2))):

	orig_lat = waypoints[x*2][0]
	orig_lon = waypoints[x*2][1]

	dest_lat = waypoints[(x*2)+2][0]
	dest_lon = waypoints[(x*2)+2][1]

	orig_string = str(orig_lat) + "%2C" + str(orig_lon)
	dest_string = str(dest_lat) + "%2C" + str(dest_lon)

	print("Origin:" + orig_string)
	print("Dest:" + dest_string)
	
	# print("SEGMENT " + str(i + 1))
	try:	
		get_info(orig_string, dest_string)
	except:
		print("Exception while trying to get_info for segment", i)
	i=i+2
	#print(i, ",", end='')


#print("\nClosing data files...")
try:
	traffic_duration_data_file.write("\n")
	ideal_duration_data_file.write("\n")
	distance_data_file.write("\n")

	traffic_duration_data_file.close()
	ideal_duration_data_file.close()
	distance_data_file.close()
except:
	print("Exception while closing data files")
print("Done")
