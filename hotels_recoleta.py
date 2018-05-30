# This example combines two collections to display the
# hotels in Buenos Aires in the neighborhood of Recoleta
import json
import numpy as np
from pymongo import MongoClient

# Connect to reficio database on MongoDB server
def Database():
    server = '192.168.0.6'
    port = 27017
    conn = MongoClient(server, port)
    return conn.reficio

db = Database()

# GPX heading

gpx = open("hotels_recoleta.gpx", "w")
gpx.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
gpx.write("<gpx version=\"1.1\" " + \
          "creator=\"Reficio - http://reficio.cc\" " + \
          "xmlns=\"http://www.topografix.com/GPX/1/1\" " + \
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " + \
          "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 " + \
          "http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
gpx.write("\t<metadata>\n")
gpx.write("\t\t<name>Hotels in Buenos Aires in the neighborhood of Recoleta</name>\n")
gpx.write("\t\t<desc>Buenos Aires Data + Geonames</desc>\n")
gpx.write("\t\t<author>\n")
gpx.write("\t\t\t<name>Halley Pacheco de Oliveira</name>\n")
gpx.write("\t\t\t<email id=\"halleypo\" domain=\"gmail.com\" />\n")
gpx.write("\t\t\t<link href=\"http://reficio.cc/\">\n")
gpx.write("\t\t\t\t<text>Reficio</text>\n")
gpx.write("\t\t\t</link>\n")
gpx.write("\t\t</author>\n")
gpx.write("\t</metadata>\n")

def wpt(name, desc, lat, lon):
    gpx.write("\t<wpt lat=\"" + lat + "\" lon=\"" + lon + "\">\n")
    gpx.write("\t\t<name>" + name + "</name>\n")
    gpx.write("\t\t<desc>" + desc + "</desc>\n")
    gpx.write("\t</wpt>\n")
    return

# Geometry of the neighborhood of Recoleta
# from the barrios_porteños collection
barrios_porteños = db.barrios_porteños
barrio =  barrios_porteños.find_one( { 'properties.BARRIO' : 'RECOLETA' } )
geometry = barrio['geometry']['coordinates']

# In geonamesar collection, find the
# hotels in Recoleta, Buenos Aires
geonamesar = db.geonamesar
hotels = []
for geoname in geonamesar.find( \
{ "$and": [ \
{ "features.geometry.coordinates": \
{ "$geoWithin": \
{ "$geometry":  \
{ "type" : "Polygon" , "coordinates": geometry } \
}  \
}  \
}, \
{ "features.properties.feature_code" : "HTL" } \
]  \
} ):
    geonameid = geoname['features'][0]['properties']['geonameid']
    name = geoname['features'][0]['properties']['name']
    lat =  geoname['features'][0]['geometry']['coordinates'][1]
    lon =  geoname['features'][0]['geometry']['coordinates'][0]
    hotels.append(np.array(name))
    wpt(name, geonameid, str(lat), str(lon))

# Print the hotels in alphabetical order
for hotel in sorted(hotels):
    print(hotel)
