# This script genaretes a gpx file for idee_faros_espana collection.
import json
import numpy as np
from pymongo import MongoClient

# GPX heading

gpx = open("idee_faros_espana.gpx", "w")
gpx.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
gpx.write("<gpx version=\"1.1\" " + \
          "creator=\"Reficio - http://reficio.cc\" " + \
          "xmlns=\"http://www.topografix.com/GPX/1/1\" " + \
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " + \
          "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 " + \
          "http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
gpx.write("\t<metadata>\n")
gpx.write("\t\t<name>Faros de España - Lighthouses of Spain</name>\n")
gpx.write("\t\t<desc>Geoportal IDEE - Infraestructura de Datos Espaciales de España</desc>\n")
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


# Connect to reficio database on MongoDB server
conn = MongoClient('localhost', 27017)
db = conn.reficio

# For all Spanish headlights
for faro in db.idee_faros_espana.find():
    print(faro)
    identificador_geografico = faro['properties']['identificador_geografico']
    id  = faro['properties']['id']
    lat = faro['geometry']['coordinates'][1]
    lon = faro['geometry']['coordinates'][0]
    wpt(identificador_geografico, id, str(lat), str(lon))

gpx.write("</gpx>")
gpx.close()
