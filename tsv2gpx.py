# This script converts a Tab Separated Value (TSV) file,
# with a single line containing the tab-separated
# name, description, latitude, and longitude
# fields, in a GPX (GPS eXchange Format) file.
#
# -*- coding: utf-8 -*-

import sys
import csv
import html
import datetime

# Input and output files
if len(sys.argv) < 2:
    print("Input file parameter is required.")
    print("Syntax: " + sys.argv[0] + " input_file")
    sys.exit()

infile = str(sys.argv[1])
filename, extension = infile.split('.')
outfile = filename + ".gpx"

# Read the TSV file
with open(infile, 'r') as tsvfile:
    fileread = csv.reader(tsvfile, delimiter='\t', quotechar='ยง')
    for tsv in fileread:
        print(tsv)
        name = tsv[0]
        desc = tsv[1]
        lat  = tsv[2]
        lon  = tsv[3]

def wpt(name, desc, lat, lon):
    gpx.write("\t<wpt lat=\"" + lat + "\" lon=\"" + lon + "\">\n")
    gpx.write("\t\t<name>" + html.escape(name) + "</name>\n")
    gpx.write("\t\t<desc>" + html.escape(desc) + "</desc>\n")
    gpx.write("\t</wpt>\n")
    return

# GPX file
gpx = open(outfile, "w")
gpx.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
gpx.write("<gpx version=\"1.1\" " + \
          "creator=\"Reficio - http://reficio.cc\" " + \
          "xmlns=\"http://www.topografix.com/GPX/1/1\" " + \
          "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " + \
          "xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 " + \
          "http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
gpx.write("\t<metadata>\n")
gpx.write("\t\t<name>" + name + "</name>\n")
gpx.write("\t\t<desc>" + desc + "</desc>\n")
gpx.write("\t\t<author>\n")
gpx.write("\t\t\t<name>Halley Pacheco de Oliveira</name>\n")
gpx.write("\t\t\t<email id=\"reficio\" domain=\"reficio.cc\" />\n")
gpx.write("\t\t\t<link href=\"http://reficio.cc/\">\n")
gpx.write("\t\t\t\t<text>Reficio</text>\n")
gpx.write("\t\t\t</link>\n")
gpx.write("\t\t</author>\n")
gpx.write("\t</metadata>\n")
wpt(name, desc, lat, lon)
gpx.write("</gpx>")
gpx.close()

#  WordPress OpenStreetMap Plugin
d = datetime.date.today()
s = "[osm_map_v3 map_center=\"" + \
    lat + "," + lon + \
    "\" zoom=\"14\" width=\"100%\" height=\"480\" " + \
    "map_border=\"thin solid grey\" " + \
    "file_list=\"../../../../wp-content/uploads/" + \
    '{:04d}'.format(d.year) + "/" + '{:02d}'.format(d.month) + \
    "/" + outfile + "\" file_color_list=\"blue\"]"
print(s)
