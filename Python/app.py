import json
import os
from start import Start
from game import Game

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_cors import CORS

import config

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


app = Flask(__name__)
CORS(app)

start = Start()


@app.route("/airport")
def get_all_airports():
    result = start.get_airports()
    json_data = json.dumps(result)
    return Response(json_data, status=200, mimetype='application/json')


@app.route("/creategame")
def create_new_game():

    # Extracting the player name from the url ...?name=""
    args = request.args
    player_name_from_url = args.get("name")

    if player_name_from_url is not None:

        # Send the player name to Start to make new database for this new game
        result = start.create_game(player_name_from_url)

        # Start returns the newly created games id
        new_game_id = json.dumps(result)

        # Insert this newly created id to Game class and get game data
        game = Game(new_game_id).check_airports_in_range()
        json_data = json.dumps(game)
        return Response(json_data, status=200, mimetype='application/json')
    else:
        return "No player name provided"


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)