import pymongo
import json

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['evan_rentals']
mongo_db.create_collection('openings')
mongo_openings_coll = mongo_db['openings']
mongo_db.create_collection('purchased_rides')
mongo_rides_coll = mongo_db['purchased_rides']

print(mongo_db.list_collection_names())

with open('bookings_list.json') as file:
    file_data = json.load(file)
if isinstance(file_data, list):
    mongo_openings_coll.insert_many(file_data)
else:
    mongo_openings_coll.insert_one(file_data)

with open('purchased_rides.json') as file:
    file_data = json.load(file)
if isinstance(file_data, list):
    mongo_rides_coll.insert_many(file_data)
else:
    mongo_rides_coll.insert_one(file_data)
cursor = mongo_rides_coll.find({})
for document in cursor:
    print(document)

