import config
import requests
import random


class Start:
    def __init__(self):
        self.all_airports = self.get_airports()
        self.start_airport = self.get_starting_airport()
        self.final_airport = self.get_final_airport()

    # Query to get starting airport
    def get_starting_airport(self):
        sql = ' select name, ident, latitude_deg, longitude_deg from airport where iso_country = "US" and type = "small_airport" and longitude_deg > -125 order by rand() limit 1;'
        cursor = config.conn.cursor(dictionary=True)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    # Query to get all airports
    def get_airports(self):
        sql = """SELECT name, ident, latitude_deg, longitude_deg, type FROM airport
                       WHERE ident = "KLAX" or ident = "KJFK" or ident = "KAUS" or ident = "KMSP" or ident = "KSEA" or ident = "KABQ" or ident = "KALN" or 
                       ident = "KBIL" or ident = "KBIS" or ident = "KCHO" or ident = "KCSG" or ident = "KGRI" or
                       ident = "KLCH" or ident = "KPTK" or ident = "KPVU";"""
        cur = config.conn.cursor(dictionary=True)
        cur.execute(sql)
        res = cur.fetchall()
        return res

    # Query to get final airport #TODO
    def get_final_airport(self):
        sql = "SELECT ident FROM airport WHERE name = 'Key West International Airport'"
        cursor = config.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # Get goals from API - The response is a list of 15 random numbers (0-5), These numbers act as goals.
    def get_random_goals_from_API(self):
        request = "https://www.randomnumberapi.com/api/v1.0/random?min=0&max=5&count=15"
        try:
            list_of_random_goal_numbers = requests.get(request).json()
        except Exception as e:
            print(f"Error occurred while requesting random goals from API: {e}")

            # If there is an error with the API - manually generate equivalent goal list
            list_of_random_goal_numbers = [random.randint(0, 5) for i in range(15)]
        return list_of_random_goal_numbers

    # Function that starts the game and prepares the database
    def create_game(self, player_name):

        # Bring the player name over from the url
        self.player_name = player_name

        # Update config name to the name from url
        config.player_name = self.player_name

        # Get a random airport from the US to use as a starting airport
        start_airport_data = self.get_starting_airport()

        # Make a new game session and insert values into status.
        self.status = {
            "id": '',
            "location": start_airport_data["name"],
            "ident": start_airport_data['ident'],
            "player_name": config.player_name,
            "latitude_deg": start_airport_data["latitude_deg"],  # Add latitude_deg to the status dictionary
            "longitude_deg": start_airport_data["longitude_deg"],  # Add longitude_deg to the status dictionary
        }

        # Insert the newly created game into the database
        sql2 = "INSERT INTO Game (location, player_range, screen_name) VALUES (%s, %s, %s)"
        cursor = config.conn.cursor()
        cursor.execute(sql2, (self.status["ident"], config.battery, self.status["player_name"]))
        config.conn.commit()

        # Generate new id for the game
        game_id = cursor.lastrowid
        self.status['id'] = game_id

        # KUN SELAAT DB -PORTS TAULUKKOA, SARAKE "ID" EI TOIMI. VERTAILE PORTS JA GAME TAULUN SARAKKEITA!
        # KUN SELAAT DB -PORTS TAULUKKOA, SARAKE "ID" EI TOIMI. VERTAILE PORTS JA GAME TAULUN SARAKKEITA!

        # Get random goals from API and insert them into Ports -table for the same game.
        goal_list = self.get_random_goals_from_API()
        for i, goal_id in enumerate(goal_list):

            # Update the database by iterating over goal_list and add a goal in order
            sql = "INSERT INTO ports (game, airport, goal) VALUES (%s, %s, %s);"
            cursor = config.conn.cursor(dictionary=True)
            cursor.execute(sql, (game_id, self.all_airports[i]['ident'], goal_id))

        return self.status['id']
