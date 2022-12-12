from flask import Flask, request, render_template, session, abort, flash
import os
import pymongo
import json
import requests
from werkzeug.utils import redirect
from bson.json_util import dumps, loads
from bson import ObjectId

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongoDB = mongo_client['evan_rentals']
collection_openings = mongoDB['openings']
collection_purchased = mongoDB['purchased_rides']

app = Flask(__name__,template_folder='templates', static_folder='staticFiles')

@app.route('/', methods=['GET'])
def home():
    # data = dict()
    # cursor = collection_openings.find()
    # for document in cursor:
    #     data = document
    return render_template('index2.html')


@app.route('/displayOpenings', methods=['GET'])
def returnOpenings():
    #cursor = collection_openings.find({"_id":ObjectId('63965d890a9fd79931f89e9d')})
    openings = collection_openings.find()
    return dumps(openings)

@app.route('/createBooking')
def returnRides():
    newDict = dict()
    x = 0
    y = 0
    data = collection_openings.find()
    print("data sent to page")
    for document in data:
        newDict[x] = document
        x+=1

    return render_template('create_booking.html', data = data, y = y)

@app.route('/bookingsPage')
def returnBookingsPage():
    return render_template('bookings.html')

@app.route('/retrieveBooking')
def retrieveBookingsPage():
    return render_template('retrieve_booking.html')

@app.route('/retrieveBookingQuery', methods=['GET', 'POST'])
def returnBookings():
    #take data sent through form 
    query = {'TicketID': request.form['ticketid']}
    results = collection_purchased.find_one(query)
    return dumps(results)

# @app.route('/login', methods=['POST'])
# def authenticate():

#     print(request)
#     query = {"Username": request.form['username'], "Password": request.form['password']}

#     valid_login = mongo_users_coll.count_documents(query)

#     if valid_login == 1:
#         session['logged_in'] = True
#         session['user'] = request.form['username']
#         #return userHomePage()
#     else:
#         flash('Invalid Login Attempt')
#     return home()


if __name__ == '__main__':
    # app.secret_key = os.urandom(12)
    app.run()#host='0.0.0.0', port=8008)