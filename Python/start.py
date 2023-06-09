import config
import requests
import random


# Query to get starting airport
def get_starting_airport():
    sql = ' select name, ident, latitude_deg, longitude_deg from airport where iso_country = "US" and type = "small_airport" and longitude_deg > -125 order by rand() limit 1;'
    cursor = config.conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    result['active'] = True
    return result


# Query to get all airports
def get_airports():
    sql = """SELECT name, ident, latitude_deg, longitude_deg, type FROM airport
                   WHERE ident = "KLAX" or ident = "KJFK" or ident = "KAUS" or ident = "KMKE" or ident = "KSEA" or ident = "KABQ" or ident = "KALN" or 
                   ident = "KBIL" or ident = "KBIS" or ident = "KCHO" or ident = "KCSG" or ident = "KGRI" or
                   ident = "KLCH" or ident = "KPTK" or ident = "KPVU";"""
    cur = config.conn.cursor(dictionary=True)
    cur.execute(sql)
    res = cur.fetchall()
    return res


# Get goals from API - The response is a list of 15 random numbers (0-4), These numbers act as goals.
def get_random_goals_from_API():
    request = "https://www.randomnumberapi.com/api/v1.0/random?min=0&max=4&count=15"
    try:
        list_of_random_goal_numbers = requests.get(request).json()
    except Exception as e:
        print(f"Error occurred while requesting random goals from API: {e}")

        # If there is an error with the API - manually generate equivalent goal list
        list_of_random_goal_numbers = [random.randint(0, 4) for i in range(15)]
    return list_of_random_goal_numbers


class Start:
    def __init__(self):
        self.all_airports = get_airports()
        self.start_airport = get_starting_airport()

    # Function that starts the game and prepares the database
    def create_game(self, player_name):

        # Establish starting values for the new game
        config.battery = 3000
        config.water = False
        config.food = False
        config.medicine = False
        config.solar = False

        # Bring the player name over from the url
        self.player_name = player_name
        config.player_name = self.player_name

        # Get a random airport from the US to use as a starting airport
        start_airport_data = get_starting_airport()

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

        # Get random goals from API and insert them into Ports -table for the same game.
        goal_list = get_random_goals_from_API()
        for i, goal_id in enumerate(goal_list):

            # Update the database by iterating over goal_list and add a goal in order
            sql = "INSERT INTO ports (game, airport, goal) VALUES (%s, %s, %s);"
            cursor = config.conn.cursor(dictionary=True)
            cursor.execute(sql, (game_id, self.all_airports[i]['ident'], goal_id))

        return self.status['id']