import random
import json
import os
import numpy as np
from datetime import date
from faker import Faker #pip install Faker
fake = Faker()


today = date.today()

def returnPrice():
    decimal = round(np.random.random(), 2)
    price = np.random.choice(50) + decimal
    return price

departure_times = ['6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00']

arrival_times = ['6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00']

meridiem = ['am', 'pm']

day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

month = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

stations = []
trains = []

# in_file = open("amtrack-stations.csv", "r")
with open("amtrack-stations.csv", "r") as f:
    station = f.read().splitlines()
    for x in range(10): #10 trains
        #append 10 random stations to the list
        #print(random.choice(station))
        stations.append(random.choice(station))

print(stations)

def reject_sample(lst, exception):
    while True:
        choice = random.choice(lst)
        if choice != exception:
            return choice

def opposite(meridiem):
    if (meridiem == 'am'):
        return 'pm'
    else:
        return 'am'
#def function to return a random choice
#def a function to return a random choice minus a certain value

bookings_dict = []
out_file = open("bookings_list.json", "w+")
for x in range(15):

    current_station = random.choice(stations)
    exception = reject_sample(stations, current_station)
    current_meridiem = np.random.choice(["am", "pm"], p=[0.80, 0.20])
    exception_meridiem = opposite(meridiem)


    bookings_dict.append({"Origin Station": current_station,
                   "Destination Station": exception,
                   "Departure Time": random.choice(departure_times) + "am", #+ current_meridiem, 
                   "Arrival Time": random.choice(arrival_times) + "pm", #+ exception_meridiem,
                   "Day": random.choice(day),
                   "Date": str(np.random.choice(31)),
                   "Month": np.random.choice(month),
                   "Cost": "$" + str(returnPrice())})
json.dump(bookings_dict, out_file, indent = 4)
out_file.close()
print(bookings_dict)

# user_list = []
# user_file = open("user_list.json", "w+")
# user_list.append({"Username": "admin",
#                   "Password": "password1",
#                   "First_Name": "admin",
#                   "Last_Name": "admin",
#                   "Email": "admin@google.com"})
# for x in range(10):
#     temp_first_name = random.choice(first_names)
#     temp_last_name = random.choice(last_names)
#     user_list.append({"Username": temp_first_name+temp_last_name,
#                       "Password": fake.password(),
#                       "First_Name": temp_first_name,
#                       "Last_Name": temp_last_name,
#                       "Email": temp_first_name+temp_last_name+"@"+random.choice(email_domain)})
# print(user_list)
# json.dump(user_list, user_file, indent=4)
# user_file.close()

purchased_rides = []

purchased_file = open("purchased_rides.json", "w+")
purchased_rides.append({"Name": "Evan",
                  "Date": str(today),
                  "RideID": "001",
                  "Price": "50.00",
                  "TicketID": "001"})
# for x in range(10):
#     temp_first_name = random.choice(first_names)
#     temp_last_name = random.choice(last_names)
#     user_list.append({"Username": temp_first_name+temp_last_name,
#                       "Password": fake.password(),
#                       "First_Name": temp_first_name,
#                       "Last_Name": temp_last_name,
#                       "Email": temp_first_name+temp_last_name+"@"+random.choice(email_domain)})
print(purchased_rides)
json.dump(purchased_rides, purchased_file, indent=4)
purchased_file.close()

# add auto translation of data for station data
# parse json file
# count up occurances of origin station 
# station_data = []
