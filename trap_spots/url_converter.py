import csv
import os

f = open('raw.csv')
#output_f = open("output.csv", 'a')
csvreader = csv.reader(f)

rows = [] 

for row in csvreader:
	rows.append(row)

for row in rows:
	fixed_date = ''
	url = row[0]
	date = row[1]
	for character in range(len(date)):
		if date[character] == "/":
			fixed_date += "-"
		else:
			fixed_date += date[character]
	time = row[2]
	filename = str("/home/pi/trap_spots/" + str(fixed_date) + "--" + time + ".csv")
	coords = url[26:-95]
	lat_lon = coords.split('%2C')
	try:
		output_f = open(filename, 'a')
	except:
		returned = os.system("touch " + filename)
		#print(returned)
		output_f = open(filename, 'a')
	#print(lat_lon[0] + "," + lat_lon[1] + "\n")
	output_f.write(lat_lon[0] + "," + lat_lon[1] + "\n")
	output_f.close
	

