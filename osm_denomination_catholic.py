# This script genaretes a gpx file for
#      "denomination=>catholic"
# in Open Street Map osmpoints collection.
import json
import bson
import html
import datetime
import numpy as np
from pymongo import MongoClient

# GPX file
gpxfile = "osm_denomination_catholic.gpx"
gpx = open(gpxfile, "w")
gpx.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
gpx.write("<gpx version=\"1.1\" " + \
          "creator=\"Reficio - http://reficio.cc\" " + \
          "xmlns=\"http://www.topografix.com/GPX/1/1\" " + \
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " + \
          "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 " + \
          "http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
gpx.write("\t<metadata>\n")
gpx.write("\t\t<name>OSM denomination=catholic</name>\n")
gpx.write("\t\t<desc>Open Street Map</desc>\n")
gpx.write("\t\t<author>\n")
gpx.write("\t\t\t<name>Halley Pacheco de Oliveira</name>\n")
gpx.write("\t\t\t<email id=\"reficio\" domain=\"reficio.cc\" />\n")
gpx.write("\t\t\t<link href=\"http://reficio.cc/\">\n")
gpx.write("\t\t\t\t<text>Reficio</text>\n")
gpx.write("\t\t\t</link>\n")
gpx.write("\t\t</author>\n")
gpx.write("\t</metadata>\n")

def wpt(name, desc, lat, lon):
    gpx.write("\t<wpt lat=\"" + lat + "\" lon=\"" + lon + "\">\n")
    gpx.write("\t\t<name>" + html.escape(name) + "</name>\n")
    gpx.write("\t\t<desc>" + html.escape(desc) + "</desc>\n")
    gpx.write("\t</wpt>\n")
    return

# To calculate the center of the map
minlat = 90
maxlat = -90
minlon = 180
maxlon = -180
count = 0

def minmaxlatlon(lat, lon):
    global maxlat, minlat, maxlon, minlon
    if lat > maxlat:
        maxlat = lat

    if lat < minlat:
        minlat = lat

    if lon > maxlon:
        maxlon = lon

    if lon < minlon:
        minlon = lon


# Connect to reficio database on MongoDB server
conn = MongoClient('localhost', 27017)
db = conn.reficio

# For all denomination=>catholic
regx = bson.regex.Regex('"denomination"=>"catholic"')
for property in db.osmpoints.find({"properties.other_tags" : regx }):
    tags = property['properties']['other_tags']
    name = property['properties']['name']
    osm_id = property['properties']['osm_id']
    lat = property['geometry']['coordinates'][1]
    lon = property['geometry']['coordinates'][0]
    wpt(name, osm_id, str(lat), str(lon))
    minmaxlatlon(lat, lon)

gpx.write("</gpx>")
gpx.close()


#  WordPress OpenStreetMap Plugin
medlat = (minlat + maxlat)/2
medlon = (minlon + maxlon)/2
d = datetime.date.today()
s = "[osm_map_v3 map_center=\"" + \
    str(medlat) + "," + str(medlon) + \
    "\" zoom=\"14\" width=\"100%\" height=\"480\" " + \
    "map_border=\"thin solid grey\" " + \
    "file_list=\"../../../../wp-content/uploads/" + \
    '{:04d}'.format(d.year) + "/" + '{:02d}'.format(d.month) + \
    "/" + gpxfile + "\" file_color_list=\"blue\"]"
print(s)
