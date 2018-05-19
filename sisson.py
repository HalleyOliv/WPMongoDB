# In MongoDB, searches the 'pages' collection of
# 'reficio' database for a document with title
# "Sébastien Auguste Sisson", and shows its excerpt.
import pymongo
import datetime
import pprint
from pymongo import MongoClient
conn = MongoClient('localhost', 27017)
db = conn.reficio
pages = db.pages
pprint.pprint(pages.find_one(
    { "title" : "Sébastien Auguste Sisson" },
    { "title" : 1, "excerpt" : 1 } )
)

