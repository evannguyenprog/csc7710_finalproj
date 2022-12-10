import pymongo
import json

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['w_books']
mongo_db.create_collection('books')
mongo_books_coll = mongo_db['books']
mongo_db.create_collection('users')
mongo_db.create_collection('books_rentals')
mongo_users_coll = mongo_db['users']

print(mongo_db.list_collection_names())

with open('book_list.json') as file:
    file_data = json.load(file)
if isinstance(file_data, list):
    mongo_books_coll.insert_many(file_data)
else:
    mongo_books_coll.insert_one(file_data)

with open('user_list.json') as file:
    file_data = json.load(file)
if isinstance(file_data, list):
    mongo_users_coll.insert_many(file_data)
else:
    mongo_users_coll.insert_one(file_data)
cursor = mongo_users_coll.find({})
for document in cursor:
    print(document)

