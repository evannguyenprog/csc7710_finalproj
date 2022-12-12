from flask import Flask, request, render_template, session, abort, flash
import os
import pymongo
import json
import requests
from werkzeug.utils import redirect
from bson.json_util import dumps, loads
from bson import ObjectId
import numpy as np
from datetime import date, datetime
import uuid


today = date.today()

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongoDB = mongo_client['evan_rentals']
collection_openings = mongoDB['openings']
collection_purchased = mongoDB['purchased_rides']

app = Flask(__name__,template_folder='templates', static_folder='staticFiles')

@app.route('/', methods=['GET'])
def home():
    openings = collection_openings.find()
    return render_template('index2.html', openings = openings)


@app.route('/mapReduce', methods=['GET'])
def mapReduce():
    return "map reduce here"

@app.route('/testing', methods=['GET'])
def testing():
    #cursor = collection_openings.find({"_id":ObjectId('63965d890a9fd79931f89e9d')})
    openings = collection_openings.find()
    return render_template('index.html', openings = openings)


@app.route('/bookingsPage')
def returnBookingsPage():
    return render_template('bookings.html')

@app.route('/retrieveBooking')
def retrieveBookingsPage():
    openings = collection_openings.find()
    return render_template('retrieve_booking.html', openings = openings)

@app.route('/retrieveBookingQuery', methods=['GET', 'POST'])
def returnBookings():
    #take data sent through form 
    query = {'TicketID': request.form['ticketid']}
    results = collection_purchased.find_one(query)
    return dumps(results)

@app.route('/createBooking')
def createBooking():
    openings = collection_openings.find()
    return render_template('create_booking.html',openings = openings)

@app.route('/createBookingQuery', methods=['GET', 'POST'])
def createBookingQuery():
    #querydb for price and id
    nDict = dict()
    search_id = request.form['rideid'] #to create search string with
    print(search_id)
    first_query = collection_openings.find_one({"_id":ObjectId(search_id)})
    nDict = first_query
    cost = nDict.get('Cost')
    # #cursor = collection_openings.find({"_id":ObjectId('63965d890a9fd79931f89e9d')})

    query = {'Name': request.form['name'],
            'Date': str(today),
            'RideID': ObjectId(search_id),
            'TicketID': str(uuid.uuid4()),
            'Cost': cost}
    collection_purchased.insert_one(query)
    return dumps(query)
   
@app.route('/deleteBooking', methods=['GET', 'POST'])
def deleteBooking():
    openings = collection_openings.find()
    return render_template('delete_booking.html',openings = openings)

@app.route('/deleteBookingQuery', methods=['GET', 'POST'])
def deleteBookingQuery():
    ticket_to_delete = request.form['deleteid']
    collection_purchased.delete_one({"TicketID":ticket_to_delete})
    return ("Ticket with id: [" + ticket_to_delete + "] successfully deleted.")

@app.route('/updateBooking', methods=['GET', 'POST'])
def updateBooking():
    openings = collection_openings.find()
    return render_template('update_booking.html',openings = openings)

@app.route('/updateBookingQuery', methods=['GET', 'POST'])
def updateBookingQuery():

    nDict = dict()
    search_id = request.form['newRideID'] #to create search string with
    print(search_id)
    first_query = collection_openings.find_one({"_id":ObjectId(search_id)})
    nDict = first_query
    cost = nDict.get('Cost')
    #newUUID = str(uuid.uuid4())
    query = {'TicketID': request.form['updateid']}

    updates = {"$set": {'RideID': ObjectId(request.form['newRideID']), 'Date': str(today), 'Cost': cost, }}

    collection_purchased.update_one(query, updates)

    ticket_to_update = request.form['updateid']
    return ("Ticket with id: [" + ticket_to_update + "] successfully updated.")


@app.route('/viewBookings', methods=['GET'])
def returnAllBookings():
    #cursor = collection_openings.find({"_id":ObjectId('63965d890a9fd79931f89e9d')})
    bookings = collection_purchased.find()
    return render_template('your_bookings.html', bookings = bookings)

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