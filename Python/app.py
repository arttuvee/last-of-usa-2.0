import json
import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

import config

# Retrieves .env file - Database connection information
load_dotenv()
# Database connection
config.conn = mysql.connector.connect(
         host=os.environ.get('HOST'),
         port= 3306,
         database=os.environ.get('DB_NAME'),
         user=os.environ.get('DB_USER'),
         password=os.environ.get('DB_PASS'),
         autocommit=True
         )


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
def airport():
    result = dbtest()
    return json.dumps(result)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)