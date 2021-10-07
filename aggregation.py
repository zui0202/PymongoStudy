from pymongo import MongoClient
db = MongoClient().aggregation_example
result = db.things.insert_many([{"x": 1, "tags": ["dog", "cat"]},
                                {"x": 2, "tags": ["cat"]},
                                {"x": 2, "tags": ["mouse", "cat", "dog"]},
                                {"x": 3, "tags": []}])
print(result.inserted_ids)

from bson.son import SON
pipeline = [
    {"$unwind": "$tags"},
    {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])}
]

import pprint
pprint.pprint(list(db.things.aggregate(pipeline)))

db.command('aggregate', 'things', pipeline=pipeline, explain=True)

from bson.code import Code
mapper = Code("""
              function () {
                this.tags.forEach(function(z) {
                  emit(z, 1);
                });
              }
              """)

reducer = Code("""
               function (key, values) {
                 var total = 0;
                 for (var i = 0; i < values.length; i++) {
                   total += values[i];
                 }
                 return total;
               }
               """)

result = db.things.map_reduce(mapper, reducer, "myresults")
for doc in result.find().sort("_id"):
  pprint.pprint(doc)

pprint.pprint(
    db.things.map_reduce(mapper, reducer, "myresults", full_response=True))

results = db.things.map_reduce(
    mapper, reducer, "myresults", query={"x": {"$lt": 2}})
for doc in results.find().sort("_id"):
  pprint.pprint(doc)

from bson.son import SON
pprint.pprint(
    db.things.map_reduce(
        mapper,
        reducer,
        out=SON([("replace", "results"), ("db", "outdb")]),
        full_response=True))