import json
import os
import airport

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_cors import CORS

import config
'from game import Game'
from airport import Airport

# Retrieves .env file - Database connection information
load_dotenv()

# Database connection
config.conn = mysql.connector.connect(
         host=os.environ.get('HOST'),
         port=3306,
         database=os.environ.get('DB_NAME'),
         user=os.environ.get('DB_USER'),
         password=os.environ.get('DB_PASS'),
         autocommit=True
         )

# Instantiate the Airport class
airport = Airport(ident="EFHK",name="Helsinki Vantaa Airport",latitude_deg=60.3172,longitude_deg=24.963301,type="lol", weather_description = "LOL", weather_degrees = "LOOOOOL")


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"


def dbtest():
    sql = 'SELECT * FROM airport WHERE iso_country="FI";'
    cur = config.conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    return res

@app.route("/airport")

def get_all_airports():
    result = airport.get_airports()
    print(result)
    json_data = json.dumps(result)
    return Response(json_data, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
