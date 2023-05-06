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
current_game = None


# http://127.0.0.1:3000/flyto?game=151&dest=KJFK&dist=100
@app.route('/flyto')
def flyto():
    args = request.args
    game_id = args.get("game")
    destination = args.get("dest")
    distance = args.get("dist")
    day = args.get("day")

    global current_game
    data = current_game.fly(game_id, destination, distance, day)

    return Response(json.dumps(data), status=200, mimetype='application/json')


# http://127.0.0.1:3000/creategame?name=lol
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
        global current_game
        current_game = Game(new_game_id)
        data = current_game.check_airports_in_range()

        json_data = json.dumps(data)
        return Response(json_data, status=200, mimetype='application/json')
    else:
        return "No player name provided"


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)