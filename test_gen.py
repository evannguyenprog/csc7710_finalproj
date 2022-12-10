import random
import json
import os
import numpy as np
from faker import Faker #pip install Faker
fake = Faker()

first_names = ['Liam', 'Olivia', 'Noah', 'Emma', 'Oliver', 'Charlotte', 'Elijah', 'Amelia', 'James', 'Ava', 'William',
               'Sophia', 'Benjamin', 'Isabella', 'Lucas', 'Mia', 'Henry', 'Evelyn', 'Theodore', 'Harper']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee']

first_word = ['The', 'A', 'We']
second_word = ['Octopus', 'Deer', 'Murder', 'Plane', 'Father', 'War', 'Men', 'Never', 'Trial', 'Crime']
third_word = ['Legacy', 'Sorrow', 'Beneath', 'Forever', 'Dragon', 'Fire', 'Ice', 'Blizzard', 'Storm']

genre = ['Action and adventure', 'Art/architecture', 'Alternate history', 'Autobiography', 'Anthology', 'Biography',
         'Chick lit', 'Business/economics', 'Children', 'Crafts/hobbies', 'Classic', 'Cookbook', 'Comic book',
         'Diary', 'Coming-of-age', 'Dictionary', 'Crime', 'Encyclopedia', 'Drama', 'Guide', 'Health/fitness',
         'Fantasy', 'History', 'Graphic novel', 'Home and garden', 'Historical fiction', 'Humor', 'Horror',
         'Journal', 'Mystery', 'Philosophy', 'Poetry', 'Romance', 'Textbook', 'Science fiction', 'Science',
         'Thriller', 'Sports', 'Western', 'Travel', 'Young adult', 'True crime']

email_domain = [ 'google.com', 'hotmail.com', 'yahoo.com', 'wayne.edu']

book_dict = []
out_file = open("book_list.json", "w+")
for x in range(1000):
    book_dict.append({"Book": random.choice(first_word) + " " + random.choice(second_word) + " " + random.choice(third_word),
                   "ISBN": str(random.randint(1000000000000, 999999999999999)),
		   "rental_count": 0,
                   "Genre": random.choice(genre),
                   "Author": random.choice(first_names) + " " + random.choice(last_names),
                   "DateAdded": str(fake.date_between(start_date='today', end_date='+10y')),
                   "Trending": np.random.choice(["No", "Yes"], p=[0.75, 0.25])})
json.dump(book_dict, out_file, indent = 4)
out_file.close()
print(book_dict)

user_list = []
user_file = open("user_list.json", "w+")
user_list.append({"Username": "admin",
                  "Password": "password1",
                  "First_Name": "admin",
                  "Last_Name": "admin",
                  "Email": "admin@google.com"})
for x in range(10):
    temp_first_name = random.choice(first_names)
    temp_last_name = random.choice(last_names)
    user_list.append({"Username": temp_first_name+temp_last_name,
                      "Password": fake.password(),
                      "First_Name": temp_first_name,
                      "Last_Name": temp_last_name,
                      "Email": temp_first_name+temp_last_name+"@"+random.choice(email_domain)})
print(user_list)
json.dump(user_list, user_file, indent=4)
user_file.close()