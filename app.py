from flask import Flask, send_from_directory, request, redirect, render_template
from haversine.haversine import Unit
import requests
import haversine as hs
import os
import json
import time

from werkzeug.datastructures import cache_property
from geopy.geocoders import Nominatim


app = Flask(__name__)

states_ = {
	'Alabama': requests.get("https://www.vaccinespotter.org/api/v0/states/AL.json"),
	'Alaska': requests.get("https://www.vaccinespotter.org/api/v0/states/AK.json"),
	'Arizona': requests.get("https://www.vaccinespotter.org/api/v0/states/AZ.json"),
	'Arkansas': requests.get("https://www.vaccinespotter.org/api/v0/states/AZ.json"),
	'California': requests.get("https://www.vaccinespotter.org/api/v0/states/CA.json"),
	'Colorado':requests.get("https://www.vaccinespotter.org/api/v0/states/CO.json"),
	'Connecticut':requests.get("https://www.vaccinespotter.org/api/v0/states/CT.json"),
	'Delaware': requests.get("https://www.vaccinespotter.org/api/v0/states/DE.json"),
	'District of Columbia': requests.get("https://www.vaccinespotter.org/api/v0/states/DC.json"),
	'Florida': requests.get("https://www.vaccinespotter.org/api/v0/states/DC.json"),
	'Georgia': requests.get("https://www.vaccinespotter.org/api/v0/states/GA.json"),
	'Hawaii':requests.get("https://www.vaccinespotter.org/api/v0/states/HI.json"),
	'Idaho':requests.get("https://www.vaccinespotter.org/api/v0/states/ID.json"),
	'Illinois':requests.get("https://www.vaccinespotter.org/api/v0/states/IL.json"),
	'Indiana': requests.get("https://www.vaccinespotter.org/api/v0/states/IN.json"),
	'Iowa': requests.get("https://www.vaccinespotter.org/api/v0/states/IA.json"),
	'Kansas': requests.get("https://www.vaccinespotter.org/api/v0/states/KS.json"),
	'Kentucky': requests.get("https://www.vaccinespotter.org/api/v0/states/KY.json"),
	'Louisiana': requests.get("https://www.vaccinespotter.org/api/v0/states/LA.json"),
	'Maine': requests.get("https://www.vaccinespotter.org/api/v0/states/ME.json"),
	'Maryland': requests.get("https://www.vaccinespotter.org/api/v0/states/MD.json"),
	'Michigan': requests.get("https://www.vaccinespotter.org/api/v0/states/MI.json"),
	'Minnesota': requests.get("https://www.vaccinespotter.org/api/v0/states/MN.json"),
	'Mississippi': requests.get("https://www.vaccinespotter.org/api/v0/states/MS.json"),
	'Missouri': requests.get("https://www.vaccinespotter.org/api/v0/states/MO.json"),
	'Montana': requests.get("https://www.vaccinespotter.org/api/v0/states/MT.json"),
	'Nebraska': requests.get("https://www.vaccinespotter.org/api/v0/states/NE.json"),
	'Nevada': requests.get("https://www.vaccinespotter.org/api/v0/states/NV.json"),
	'New Hampshire': requests.get("https://www.vaccinespotter.org/api/v0/states/NH.json"),
	'New Jersey': requests.get("https://www.vaccinespotter.org/api/v0/states/NJ.json"),
	'New Mexico': requests.get("https://www.vaccinespotter.org/api/v0/states/NM.json"),
	'New York': requests.get("https://www.vaccinespotter.org/api/v0/states/NM.json"),
	'North Carolina': requests.get("https://www.vaccinespotter.org/api/v0/states/NC.json"),
	'North Dakota': requests.get("https://www.vaccinespotter.org/api/v0/states/ND.json"),
	'Ohio': requests.get("https://www.vaccinespotter.org/api/v0/states/OH.json"),
	'Oklahoma': requests.get("https://www.vaccinespotter.org/api/v0/states/OK.json"),
	'Oregon': requests.get("https://www.vaccinespotter.org/api/v0/states/OR.json"),
	'Pennsylvania': requests.get("https://www.vaccinespotter.org/api/v0/states/PA.json"),
	'Puerto Rico': requests.get("https://www.vaccinespotter.org/api/v0/states/PR.json"),
	'Rhode Island': requests.get("https://www.vaccinespotter.org/api/v0/states/RI.json"),
	'South Carolina': requests.get("https://www.vaccinespotter.org/api/v0/states/SC.json"),
	'South Dakota': requests.get("https://www.vaccinespotter.org/api/v0/states/SD.json"),
	'Tennessee': requests.get("https://www.vaccinespotter.org/api/v0/states/TN.json"),
	'Texas': requests.get("https://www.vaccinespotter.org/api/v0/states/TX.json"),
	'Virgin Island': requests.get("https://www.vaccinespotter.org/api/v0/states/VI.json"),
	'Utah': requests.get("https://www.vaccinespotter.org/api/v0/states/UT.json"),
	'Vermont': requests.get("https://www.vaccinespotter.org/api/v0/states/VT.json"),
	'Virginia': requests.get("https://www.vaccinespotter.org/api/v0/states/VA.json"),
	'Washington': requests.get("https://www.vaccinespotter.org/api/v0/states/WA.json"),
	'West Virginia': requests.get("https://www.vaccinespotter.org/api/v0/states/WV.json"),
	'Wisconsin':requests.get("https://www.vaccinespotter.org/api/v0/states/WI.json"),
	'Wyoming': requests.get("https://www.vaccinespotter.org/api/v0/states/WY.json")
}


def fetch_then_cache(url, name):
	cachepath = os.path.join('cache', name)
	if not os.path.exists('cache'):
		os.mkdir('cache')
	if os.path.exists(cachepath):
		with open(cachepath, 'r') as f:
			return json.loads(f.read())
	response = requests.get(url)
	data = response.json()
	with open(cachepath, 'w') as f:
			return f.write(json.dumps(data))
	return data

@app.route('/') #route decorator for server to run this html code then give to browser
def index():
	return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>') #wildcard to make sure everything after path is captured
def static_assets(path: str):
	return send_from_directory('static', path)


#retrieves location from UI 
@app.route('/get_user_location', methods=['POST'])
def get_user_location():
	global location1
	global get_locs
	
	loc = request.form["result"]
	loc = loc.split(",")
	lat = float(loc[0])
	
	long = float(loc[1])
	
	state_information = state_of_user((lat,long))
	state_location = states_[state_information].json()
	
	get_loc = getLocations(state_location,(lat,long))
	max_index = len(get_loc)
	return render_template('locations.html', locations= get_loc, index=0, max_index= int(max_index))

def state_of_user(coordinates):
    # CHANGING LAT&LONG TO ADDRESS
    locator = Nominatim(user_agent= "myGeocoder")
    # location we get from the website
    location = locator.reverse(coordinates)
    state_of_user = location.raw["address"]
    return state_of_user['state']

@app.route('/get_next_locations', methods=['POST'])
def get_next_locations():
	locations = request.form["locations"]
	index = request.form["index"]
	max_index = request.form["max_index"]
	return render_template('locations.html', locations=json.loads(locations), index=int(index) + 10, max_index= int(max_index))

@app.route('/get_previous_locations', methods=['POST'])
def get_previous_locations():
	locations = request.form["locations"]
	index = request.form["index"]
	max_index = request.form["max_index"]
	return render_template('locations.html', locations=json.loads(locations), index=max(0, int(index) - 10),max_index= int(max_index))

#this function uses haversine library to calculate distance between two coordinates and sorts them based on closest location

def getLocations(state, coord):
	i = 0
	places = []

	for providers in state['features']:
		spot_latlong = (providers['geometry']['coordinates'][1], providers['geometry']['coordinates'][0])
		if((hs.haversine(coord, spot_latlong))<=5): #in km
			places.append([providers['properties']['name'],providers['properties']['url'],providers['properties']['address'],providers['properties']['city'],providers['properties']['state'],hs.haversine(coord, spot_latlong)])
			i = i+1
	
	# print("i",i)
	places.sort(key = lambda x:x[5])
	return places
	


print('Breakpoint me!')
# all_states = {}

if __name__ == '__main__':
	app.run('127.0.0.1', int(os.environ.get('PORT', 2000)), True)
