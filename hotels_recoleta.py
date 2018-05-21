# This example combines two collections to display the
# hotels in Buenos Aires in the neighborhood of Recoleta
import json
import numpy as np
from pymongo import MongoClient

# Connect to reficio database on MongoDB server
conn = MongoClient('localhost', 27017)
db = conn.reficio

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
}, {"features.properties.name": 1, "_id" : 0} ):
    hotels.append(np.array(geoname['features'][0]['properties']['name']))

# Print the hotels in alphabetical order
for hotel in sorted(hotels):
    print(hotel)
