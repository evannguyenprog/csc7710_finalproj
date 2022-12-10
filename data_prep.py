import random
import json
import os
import numpy as np
from faker import Faker #pip install Faker
fake = Faker()

departure_times = ['6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00']

arrival_times = ['6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00']

meridiem = ['am', 'pm']

week = [] #iterate random value between 1 and 31

day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

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

#def function to return a random choice
#def a function to return a random choice minus a certain value

# bookings_list = []
# out_file = open("bookings_list.json", "w+")
# for x in range(200):

#     current_station = random.choice(stations)
#     exception = reject_sample(stations, current_station)
#     book_dict.append({"Origin Station": current_station,
#                    "Destination Station": exception,
#                    "Departure Time": random.choice(genre),
#                    "Arrival Time": random.choice(first_names) + " " + random.choice(last_names),
#                    "Date": np.random.choice(["No", "Yes"], p=[0.75, 0.25])})
# json.dump(book_dict, out_file, indent = 4)
# out_file.close()
# print(book_dict)

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