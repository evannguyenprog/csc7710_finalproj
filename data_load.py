import pymongo
import json

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['evan_rentals']
mongo_db.create_collection('openings')
mongo_openings_coll = mongo_db['openings']

mongo_db.create_collection('purchased_rides')
mongo_rides_coll = mongo_db['purchased_rides']

mongo_db.create_collection('station_data')
mongo_station_coll = mongo_db['station_data']


print(mongo_db.list_collection_names())

#load in bookings list and insert into db
with open('bookings_list.json') as file:
    file_data = json.load(file)
if isinstance(file_data, list):
    mongo_openings_coll.insert_many(file_data)
else:
    mongo_openings_coll.insert_one(file_data)

#load in purchased rides list and insert into db
with open('purchased_rides.json') as file:
    file_data = json.load(file)
if isinstance(file_data, list):
    mongo_rides_coll.insert_many(file_data)
else:
    mongo_rides_coll.insert_one(file_data)
cursor = mongo_rides_coll.find({})
for document in cursor:
    print(document)


#load in station data and insert into db
with open('station_data.json') as file:
    file_data = json.load(file)
if isinstance(file_data, list):
    mongo_station_coll.insert_many(file_data)
else:
    mongo_station_coll.insert_one(file_data)
cursor = mongo_station_coll.find({})
for document in cursor:
    print(document)

