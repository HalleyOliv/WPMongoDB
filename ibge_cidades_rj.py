# This script genaretes a gpx file for the cities of the
# State of Rio de Janeiro using the ibgelocalidades collection.
import json
import html
import numpy as np
from pymongo import MongoClient

# GPX heading

gpx = open("ibge_cidades_rj.gpx", "w")
gpx.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
gpx.write("<gpx version=\"1.1\" " + \
          "creator=\"Reficio - http://reficio.cc\" " + \
          "xmlns=\"http://www.topografix.com/GPX/1/1\" " + \
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " + \
          "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 " + \
          "http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
gpx.write("\t<metadata>\n")
gpx.write("\t\t<name>Cidades do Estado do Rio de Janeiro - Cities of the State of Rio de Janeiro</name>\n")
gpx.write("\t\t<desc>IBGE (Instituto Brasileiro de Geografia e Estatística / Brazilian Institute of Geography and Statistics)</desc>\n")
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

# Connect to reficio database on MongoDB server
conn = MongoClient('localhost', 27017)
db = conn.reficio

# For cities in Rio de Janeiro
for city in db.ibgelocalidades.find({ "$and": \
[{'properties.NM_UF' : 'RIO DE JANEIRO'}, \
{'properties.NM_CATEGOR' : 'CIDADE'}]}):
    name = city['properties']['NM_MUNICIP']
    desc = city['properties']['NM_MICRO'] + " - " + city['properties']['NM_MESO']
    lat  = city['geometry']['coordinates'][1]
    lon  = city['geometry']['coordinates'][0]
    print(name + " - " + desc)
    wpt(name, desc, str(lat), str(lon))

gpx.write("</gpx>")
gpx.close()
