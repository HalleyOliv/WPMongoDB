# Bing - Find a Location by Query
# https://msdn.microsoft.com/en-us/library/ff701711.aspx
#
# This script shows how to find the location of Central do Brasil
# (Terminal Central Station, Rio de Janeiro, Brazil) using a query
# to obtain the latitude and longitude coordinates that correspond
# to this location.
#
# -*- coding: utf-8 -*-

import http.client, urllib.parse
import json

# Read the Bing Maps Key from file 'BingMapsKey.txt'
BingMapsKey = open('BingMapsKey.txt', 'r').read().rstrip("\n")

host = 'dev.virtualearth.net'
path = '/REST/v1/Locations'
locationQuery = 'Central do Brasil'

params = '?query=' + urllib.parse.quote (locationQuery) + \
         '&key=' + BingMapsKey

def get_locations ():
    headers = {}
    conn = http.client.HTTPSConnection (host)
    conn.request ("GET", path + params, None, headers)
    response = conn.getresponse ()
    return response.read ()

result = get_locations ()
print (json.dumps(json.loads(result), indent=4))
