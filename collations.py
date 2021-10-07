'''
Data structure is as follows:
Collation(locale=<string>,
          caseLevel=<bool>,
          caseFirst=<string>,
          strength=<int>,
          numericOrdering=<bool>,
          alternate=<string>,
          maxVariable=<string>,
          backwards=<bool>)
'''

from pymongo import MongoClient
from pymongo.collation import Collation

db = MongoClient().test
collection = db.create_collection('contacts',
                                  collation=Collation(locale='fr_CA'))

from pymongo import MongoClient
from pymongo.collation import Collation

contacts = MongoClient().test.contacts
contacts.create_index('name',
                      unique=True,
                      collation=Collation(locale='fr_CA'))

from pymongo import MongoClient
from pymongo.collation import Collation

collection = MongoClient().test.contacts
docs = collection.find({'city': 'New York'}).sort('name').collation(
    Collation(locale='fr_CA'))

from pymongo import MongoClient
from pymongo.collation import Collation, CollationStrength

contacts = MongoClient().test.contacts
result = contacts.update_many(
    {'first_name': 'jürgen'},
    {'$set': {'verified': 1}},
    collation=Collation(locale='de',
                        strength=CollationStrength.SECONDARY))