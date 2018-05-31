# Google Maps Platform - Web Services - Geocoding API
# https://developers.google.com/maps/documentation/geocoding/start?hl=en
#
# This Python script shows how to geolocalize the address
# Igreja de Nossa Senhora da Candelária - Praça Pio X - Centro,
# Rio de Janeiro - RJ (Church of Our Lady of Candelaria)
# accessing Google Maps Geocoding API through an HTTP interface,
# and creates a GPX (GPS Exchange Format) file to display the
# address on the map using the OpenStreetMap.
#
# -*- coding: utf-8 -*-

import http.client, urllib.parse
import html
import json

# Read the Google Maps Key from 'GoogleMapsKey.txt' file
GoogleMapsKey = open('GoogleMapsKey.txt', 'r').read().rstrip("\n")

host = 'maps.googleapis.com'
path = '/maps/api/geocode/json'
address = 'Igreja de Nossa Senhora da Candelária - Praça Pio X'

params = '?address=' + urllib.parse.quote (address) + \
         '&key=' + GoogleMapsKey

def wpt(name, desc, lat, lon):
    gpx.write("\t<wpt lat=\"" + lat + "\" lon=\"" + lon + "\">\n")
    gpx.write("\t\t<name>" + html.escape(name) + "</name>\n")
    gpx.write("\t\t<desc>" + html.escape(desc) + "</desc>\n")
    gpx.write("\t</wpt>\n")
    return

def get_response():
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path + params)
    response = conn.getresponse()
    return response.read()

results = json.loads(get_response())
print(json.dumps(results, indent=4))
formatted_address = results['results'][0]['formatted_address']
lat = str(results['results'][0]['geometry']['location']['lat'])
lon = str(results['results'][0]['geometry']['location']['lng'])

# GPX

gpx = open("google_maps_candelaria.gpx", "w")
gpx.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
gpx.write("<gpx version=\"1.1\" " + \
          "creator=\"Reficio - http://reficio.cc\" " + \
          "xmlns=\"http://www.topografix.com/GPX/1/1\" " + \
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " + \
          "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 " + \
          "http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
gpx.write("\t<metadata>\n")
gpx.write("\t\t<name>" + address + "</name>\n")
gpx.write("\t\t<desc>" + formatted_address + "</desc>\n")
gpx.write("\t\t<author>\n")
gpx.write("\t\t\t<name>Halley Pacheco de Oliveira</name>\n")
gpx.write("\t\t\t<email id=\"reficio\" domain=\"reficio.cc\" />\n")
gpx.write("\t\t\t<link href=\"http://reficio.cc/\">\n")
gpx.write("\t\t\t\t<text>Reficio</text>\n")
gpx.write("\t\t\t</link>\n")
gpx.write("\t\t</author>\n")
gpx.write("\t</metadata>\n")
wpt(address, formatted_address, lat, lon)
gpx.write("</gpx>")
gpx.close()
