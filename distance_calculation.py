import os
import io 
import json 
import requests
import math

file = open('key.txt','r')
key = file.read().strip()


origin = '3100+14TH+ST+NW+WASHINGTON+DC+20010'
destinations = '2000+M+STREET+NW+WASHINGTON+DC+20036 | 28+KENNEDY+STREET+NW+WASHINGTON+DC+20011'

def closest_vaccination_area(origin_address,destinations):
    '''
    This function takes in the origin address(location of the user) 
    in the following format:
    3100+14TH+ST+NW+WASHINGTON+DC+20010 
    And the destination(vaccination spot/spots) in the following format:
    2000+M+STREET+NW+WASHINGTON+DC+20036 | 28+KENNEDY+STREET+NW+WASHINGTON+DC+20011 
    This symbol '|' is used as a separator between the addresses.
    This function returns the closest address to the origin.
    '''
    url = ('https://maps.googleapis.com/maps/api/distancematrix/json'
            + '?language=en-US&units=imperial'
            + '&origins={}'
            + '&destinations={}'
            + '&key={}'
            ).format(origin, destinations, key)
    r = requests.get(url)
    result = r.json()
    closest_distance = math.inf
    for i in range(len(result['rows'][0]['elements'])):
        current_distance = result['rows'][0]['elements'][i]['distance']['text'] 
        current_distace = current_distance.split(' ')
        if float(current_distace[0]) < closest_distance:
            closest_distance = float(current_distace[0])
            closest_destination = result['destination_addresses'][i]
    origin_address = origin_address.replace('+',' ')
    return {'origin_address':origin_address,'closest_vaccination_address':closest_destination}