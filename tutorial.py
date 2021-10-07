import pymongo

from pymongo import MongoClient
client = MongoClient()

#same as
# client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://localhost:27017/')

db = client.test_database
# same as
# db = client['test-database']

collection = db.test_collection
#same as
# collection = db['test-collection']

import datetime
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

print(db.list_collection_names())

import pprint
pprint.pprint(posts.find_one())

pprint.pprint(posts.find_one({"author": "Mike"}))

posts.find_one({"author": "Eliot"})

print(post_id)
pprint.pprint(posts.find_one({"_id": post_id}))

post_id_as_str = str(post_id)
posts.find_one({"_id": post_id_as_str}) # no result

from bson.objectid import ObjectId

# The web framework gets post_id from the URL and passes it as a string
def get(post_id):
    # Convert from string to ObjectId:
    document = client.db.collection.find_one({'_id': ObjectId(post_id)})

new_posts = [{"author": "Mike",
              "text": "Another post!",
              "tags": ["bulk", "insert"],
              "date": datetime.datetime(2009, 11, 12, 11, 14)},
             {"author": "Eliot",
              "title": "MongoDB is fun",
              "text": "and pretty easy too!",
              "date": datetime.datetime(2009, 11, 10, 10, 45)}]
result = posts.insert_many(new_posts)
print(result.inserted_ids)

for post in posts.find():
  pprint.pprint(post)

for post in posts.find({"author": "Mike"}):
   pprint.pprint(post)

print(posts.count_documents({}))
print(posts.count_documents({"author": "Mike"}))

d = datetime.datetime(2009, 11, 12, 12)
for post in posts.find({"date": {"$lt": d}}).sort("author"):
  pprint.pprint(post)

result = db.profiles.create_index([('user_id', pymongo.ASCENDING)],
                                  unique=True)
sorted(list(db.profiles.index_information()))

user_profiles = [
    {'user_id': 211, 'name': 'Luke'},
    {'user_id': 212, 'name': 'Ziltoid'}]
result = db.profiles.insert_many(user_profiles)

new_profile = {'user_id': 213, 'name': 'Drew'}
duplicate_profile = {'user_id': 212, 'name': 'Tommy'}
result = db.profiles.insert_one(new_profile)  # This is fine.
# result = db.profiles.insert_one(duplicate_profile)