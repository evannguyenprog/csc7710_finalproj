from flask import Flask, request, render_template, session, abort, flash
import os
import pymongo
import json
import requests
from werkzeug.utils import redirect

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['evan_rentals']
mongo_users_coll = mongo_db['users']

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        user_profile = requests.get("http://127.0.0.1:5003/users/{}".format(session.get('user')))
        user_profile = user_profile.json()
        welcome_message = "Welcome " + user_profile["First_Name"] + "!"
        return welcome_message
        
@app.route('/login', methods=['POST'])
def authenticate():

    print(request)
    query = {"Username": request.form['username'], "Password": request.form['password']}

    valid_login = mongo_users_coll.count_documents(query)

    if valid_login == 1:
        session['logged_in'] = True
        session['user'] = request.form['username']
        #return userHomePage()
    else:
        flash('Invalid Login Attempt')
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8008)