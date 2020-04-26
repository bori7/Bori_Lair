
'''
cd C:\
md "\data\db"
"C:\Program Files\MongoDB\Server\4.2\bin\mongod.exe" --dbpath="c:\data\db"
"C:\Program Files\MongoDB\Server\4.2\bin\mongo.exe"'''

'''
import pymongo
from pymongo import MongoClient

client = MongoClient()


db = client.test_database

db = client['test-database']

collection = db.test_collection

collection = db['test-collection']

import datetime

post = {'author' : 'bori',
        'text':"my first database!!!",
        'tags': ['mongodb','python','pymongo'],
        'date': datetime.datetime.utcnow()}

posts  = db.posts

post_id = posts.insert_one(post).inserted_id

post_id

db.list_collection_names()

import pprint

#pprint.pprint(posts.find_one())

#pprint.pprint(posts.find_one({"author":'mike'}))

#pprint.pprint(posts.find_one({'_id': post_id}))

post_id_as_str = str(post_id)

#posts.find_one({"_id" : post_id_as_str})

from bson.objectid import ObjectId

def get(post_id):
        document = client.db.collection.find_one({'_id':ObjectId(post_id)})

new_posts = [{'author' : "Mike",
              "text": "Another post!",
              "tags" : ["bulk", "insert"],
              "date": datetime.datetime(2009,11,12,11,14)},
             {'author' : "Eliot",
              "title" : "MongoDB is fun",
              "text" : "and pretty easy too!",
              "date": datetime.datetime(2009, 11, 10, 10, 45)}]


#result = posts.insert_many(new_posts)

#result.inserted_ids

for post in posts.find():
        pass
        #pprint.pprint(post)

#pprint.pprint(posts.count_documents({}))

#pprint.pprint(posts.count_documents({"author":"Mike"}))

d = datetime.datetime(2009, 11, 12, 12)

for post in posts.find({"date":{"$lt":d}}).sort("author"):
        pass
        #pprint.pprint(post)

result = db.profiles.create_index([('user_id', pymongo.ASCENDING)],
                                  unique = True)

#pprint.pp(sorted(list(db.profiles.index_information())))


user_profiles = [
        {'user_id' : 211, 'name':'luke'},
        {'user_id' : 212,  'name': 'Ziltoid'}]

result = db.profiles.insert_many(user_profiles)

new_profile = {'user_id': 213, 'name':'Drew'}
duplicate_profile = {'user_id':212, 'name': 'Tommy'}

result = db.profiles.insert_one(new_profile)
result = db.profiles.insert_one(duplicate_profile)


'''

from pymongo import MongoClient

db  = MongoClient().aggregation_example
result = db.things.insert_many([{"x": 1, "tags": ["dog","cat"]},
                                {"x":2, "tags" : ["cat"]},
                                {"x":2 , "tags" : ["mouse", "cat", "dog"]},
                                {"x": 3, "tags":[]}])

result.inserted_ids

from bson.son import SON

pipeline = [
        {"$unwind" : "$tags"},
        {"$group" : {"_id":"$tags", "count": {"$sum":1}}},
        {"$sort": SON([("count", -1),("_id",-1)])}
]
import pprint
pprint.pprint(list(db.things.aggregate(pipeline)))

db.command('aggregate', 'things', pipeline = pipeline, explain = True)

from bson.code import code
mapper = Code("""
function() {
this.tags.forEach(function(z){
emit(z,1);
});
""")



