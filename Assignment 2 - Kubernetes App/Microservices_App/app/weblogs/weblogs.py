from __future__ import print_function
from flask import Flask, render_template, jsonify

import json
from bson import json_util

import re
import sys

import time
from time import sleep

import pymongo
from pymongo import MongoClientS

app = Flask(__name__)

data = ''
key_count = 1
max_count = 30000

# Function to make MongoDB Connection
def get_db():
    client = MongoClient(host='test-mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")

    db = client["analytics_db"]

    return db

# Function to parse BSON data from Mongo
def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/update_data', methods=['POST'])
def updatedata():

    time.sleep(1)

    global data
    global key_count
    global max_count

    db= ""

    db = get_db()

    key_count += 1
    
    for x in db['analytics_tb'].find({"id": key_count}):

        data = x
        data = parse_json(data)

        if key_count == max_count:
            break

    return jsonify(data, render_template('data_model.html', x=data))

@app.route('/')
def get_page():
    return render_template('test.html', x=data)

def serverlessfunc(event, context):
  return key_count

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')