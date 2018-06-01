# This script genaretes a gpx file for the perimeter of Recoleta
import json
import html
import numpy as np
from pymongo import MongoClient

# Connect to reficio database on MongoDB server
def Database():
    server = 'localhost'
    port = 27017
    conn = MongoClient(server, port)
    return conn.reficio

db = Database()

# GPX heading

gpx = open("perimeter_recoleta.gpx", "w")
gpx.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
gpx.write("<gpx version=\"1.1\" " + \
          "creator=\"Reficio - http://reficio.cc\" " + \
          "xmlns=\"http://www.topografix.com/GPX/1/1\" " + \
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " + \
          "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 " + \
          "http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
gpx.write("\t<metadata>\n")
gpx.write("\t\t<name>Perimeter of Recoleta</name>\n")
gpx.write("\t\t<desc>Buenos Aires Data</desc>\n")
gpx.write("\t\t<author>\n")
gpx.write("\t\t\t<name>Halley Pacheco de Oliveira</name>\n")
gpx.write("\t\t\t<email id=\"reficio\" domain=\"reficio.cc\" />\n")
gpx.write("\t\t\t<link href=\"http://reficio.cc/\">\n")
gpx.write("\t\t\t\t<text>Reficio</text>\n")
gpx.write("\t\t\t</link>\n")
gpx.write("\t\t</author>\n")
gpx.write("\t</metadata>\n")
gpx.write("\t<trk>\n")
gpx.write("\t\t<name>GPS data</name>\n")
gpx.write("\t\t<trkseg>\n")

def trkpt(lat, lon):
    gpx.write("\t\t\t<trkpt lat=\"" + lat + "\" lon=\"" + lon + "\"></trkpt>\n")
    return

# Perimeter of Recoleta coordinates
barrios_porteños = db.barrios_porteños
barrio =  barrios_porteños.find_one( { 'properties.BARRIO' : 'RECOLETA' } )
geometry = barrio['geometry']['coordinates']

for geo in geometry[0]:
    trkpt(str(geo[1]),str(geo[0]))

gpx.write("\t\t</trkseg>\n")
gpx.write("\t</trk>\n")
gpx.write("</gpx>")
gpx.close()
