from flask import Flask, render_template, jsonify

import redis
import re
import sys

app = Flask(__name__)

data = ''

@app.route('/update_data', methods=['POST'])
def updatedata():

    data = ''

    try:
        conn = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
        for key in conn.scan_iter():
            value = conn.get(key)

            data = str(key) + value

            print(data, flush=True)

    except Exception as ex:
        data = 'Error:' + str(ex)
    return jsonify('', render_template('data_model.html', x=data))

@app.route('/')
def get_page():
    return render_template('index.html', x=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
