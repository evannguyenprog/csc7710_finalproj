from flask import Flask, request, render_template, session, abort, flash
import os
import pymongo
import json
import requests
from werkzeug.utils import redirect
from bson.json_util import dumps, loads
from bson import ObjectId, Code
import numpy as np
from datetime import date, datetime
import uuid


today = date.today()

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongoDB = mongo_client['evan_rentals']
collection_openings = mongoDB['openings']
collection_purchased = mongoDB['purchased_rides']
collection_station_data = mongoDB['station_data']

app = Flask(__name__,template_folder='templates', static_folder='staticFiles')

@app.route('/', methods=['GET'])
def home():
    openings = collection_openings.find()
    return render_template('index2.html', openings = openings)


@app.route('/mapReduce', methods=['GET'])
def mapReduce():
    station_data = collection_station_data.find()

    result = mongo_client['evan_rentals']['station_data'].aggregate([
        {
            '$project': {
                '_id': 0, 
                'TicketIDs': 1, 
                'Origin Station': 1
            }
        }, {
            '$project': {
                '_id': '$Origin Station', 
                'ticket_count': {
                    '$size': '$TicketIDs'
                }
            }
        }])

    return render_template('map_reduce.html', stationdata = station_data, mapreduce = result)

# @app.route('/mapReduceQuery', methods=['GET', 'POST'])
# def mapReduceQuery():
#     map = Code("function () {"
#         "  this.RidesIDs.forEach(function() {"
#         "    emit('TicketID', 1);"
#         "  });"
#         "}")
#     reduce = Code("function (key, values) {"
#             "  var total = 0;"
#             "  for (var i = 0; i < values.length; i++) {"
#             "    total += values[i];"
#             "  }"
#             "  return total;"
#             "}")
#     result = collection_station_data.map_reduce(map, reduce, "results")

    
#     return dumps(result) 

@app.route('/testing', methods=['GET'])
def testing():
    #cursor = collection_openings.find({"_id":ObjectId('63965d890a9fd79931f89e9d')})
    # query2 = {"RidesIDs": {"$in" : ["63965d890a9fd79931f89e9d"]} }
    # # query2 = {'_id': ObjectId('63970ea26bb2ab120052312e')}
    # updates = {"$push": {'TicketIDs': '20'}}
    # collection_station_data.update_one(query2, updates)
    return "testing"


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
    first_query = collection_openings.find_one({"_id":ObjectId(search_id)})
    nDict = first_query
    cost = nDict.get('Cost')
    # #cursor = collection_openings.find({"_id":ObjectId('63965d890a9fd79931f89e9d')})
    newUUID = str(uuid.uuid4())
    print(search_id)
    print(newUUID)
    query = {'Name': request.form['name'],
            'Date': str(today),
            'RideID': ObjectId(search_id),
            'TicketID': newUUID,
            'Cost': cost}
    collection_purchased.insert_one(query)
    
    #update the station data so it accurately reflects which stations have which tickets 
    query2 = {"RidesIDs": {"$in" : [search_id]} }
    updates = {"$push": {'TicketIDs': newUUID}}
    collection_station_data.update_one(query2, updates)
    return dumps(query2)
   
@app.route('/deleteBooking', methods=['GET', 'POST'])
def deleteBooking():
    bookings = collection_purchased.find()
    return render_template('delete_booking.html',bookings = bookings)

@app.route('/deleteBookingQuery', methods=['GET', 'POST'])
def deleteBookingQuery():
    #delete ticket from bookings
    ticket_to_delete = request.form['deleteid']
    collection_purchased.delete_one({"TicketID":ticket_to_delete})
    #delete ticket from station data
    query = {"TicketIDs": {"$in" : [ticket_to_delete]} }
    updates = {"$pull": {'TicketIDs': ticket_to_delete}}
    collection_station_data.update_one(query, updates)
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

if __name__ == '__main__':
    app.run()