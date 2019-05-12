#!/usr/bin/python3
#import modules needed, store in URL that has the JSON we want to parse
#get the content of the url and store it in data using the json module
import requests, json, datetime
import config
url = 'https://gbfs.capitalbikeshare.com/gbfs/en/station_status.json'
r = requests.get(url)
data = json.loads(r.content.decode('utf-8'))

#initialize the dictionaries where we will store all the information that we will access
numBikes = dict()
numDocks = dict()
numBikesE = dict()

#Loop through all the stations and extract bikes, ebikes, docks and put them in their
#respective dictionary with the station id being the key
for item in data["data"]["stations"]: #we drill down to the station level here
    station = item["station_id"] #here we get all the station ids and store them in the station variable
    bikes = item["num_bikes_available"]
    docks = item["num_docks_available"]
    ebikes = item["num_ebikes_available"]
    numBikes[station] = bikes #here we fill in the dict with the bikes for all the stations
    numDocks[station] = docks
    numBikesE[station] = ebikes

#Here we pull out the data points from the 2 stations we actually care about
#we found the station IDs by manually looking at the JSON earlier
WorkBikes = numBikes["443"]
KennedyBikes = numBikes["77"]
WorkBikesE = numBikesE["443"]
KennedyBikesE = numBikesE["77"]
WorkDocks = numDocks["443"]
KennedyDocks = numDocks["77"]

#now we initialize the array we will store the data we want to send to ifttt
#based on the time of day we will check certain stations
spaces = "     " #this will give us some space between each entry cz ifttt doesn't have spaces
WtoK = "\nWork --> Kennedy"
KtoW = "\nKennedy --> Work"
report = {}
now = datetime.datetime.now()
if now.hour > 15:
    report["value1"] = str(WorkBikes) + spaces
    report["value2"] = str(WorkBikesE) + spaces
    report["value3"] = str(KennedyDocks) + WtoK
else :
    report["value1"] = str(KennedyBikes) + spaces
    report["value2"] = str(KennedyBikesE) + spaces
    report["value3"] = str(WorkDocks) + KtoW

#we populated the array and now we send to this webhook which triggers the ios notification in ifttt
requests.post("https://maker.ifttt.com/trigger/cabi_status/with/key/" + config.webhook_key, data=report)

