import config
import string,random


class Start:
    def __init__(self):
        self.all_airports = self.get_airports()
        self.start_airport = self.starting_airport()
        self.final_airport = self.final_airport()

    def starting_airport(self):
        sql = ' select name, ident, latitude_deg, longitude_deg from airport where iso_country = "US" and type = "small_airport" and longitude_deg > -125 order by rand() limit 1;'
        cursor = config.conn.cursor(dictionary=True)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    def get_airports(self):
        sql = """SELECT name, ident, latitude_deg, longitude_deg, type FROM airport
                       WHERE ident = "KLAX" or ident = "KJFK" or ident = "KAUS" or ident = "KMSP" or ident = "KSEA" or ident = "KABQ" or ident = "KALN" or 
                       ident = "KBIL" or ident = "KBIS" or ident = "KCHO" or ident = "KCSG" or ident = "KGRI" or
                       ident = "KLCH" or ident = "KPTK" or ident = "KPVU";"""
        cur = config.conn.cursor(dictionary=True)
        cur.execute(sql)
        res = cur.fetchall()
        return res

    def final_airport(self):
        sql = "SELECT ident FROM airport WHERE name = 'Key West International Airport'"
        cursor = config.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def get_goals(self):
        sql = "SELECT * from goal;"
        cursor = config.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # Function that starts the game and prepares the database
    def create_game(self):
        # Get a random airport from the US to use as a starting airport
        sql1 = ' select name, ident, latitude_deg, longitude_deg from airport where iso_country = "US" and type = "small_airport" and longitude_deg > -125 order by rand() limit 1;'
        cursor = config.conn.cursor(dictionary=True)
        cursor.execute(sql1)
        start_airport_data = cursor.fetchone()

        # Make a new game session and insert values into status.
        self.status = {
            "id": ''.join(str(random.randint(0, 9)) for i in range(5)),
            "location": start_airport_data["name"],
            "player_name": config.default_name,
            "latitude_deg": start_airport_data["latitude_deg"],  # Add latitude_deg to the status dictionary
            "longitude_deg": start_airport_data["longitude_deg"],  # Add longitude_deg to the status dictionary
            "food_collected": config.food,
            "water_collected": config.water,
            "solar_collected": config.solar,
            "medicine_collected": config.medicine,
            "battery_range": config.battery,
            "days_left": config.days_left
        }

        # Query for all airports that the game uses.
        sql3 = """SELECT name, ident, latitude_deg, longitude_deg, type FROM airport
                       WHERE ident = "KLAX" or ident = "KJFK" or ident = "KAUS" or ident = "KMSP" or ident = "KSEA" or ident = "KABQ" or ident = "KALN" or 
                       ident = "KBIL" or ident = "KBIS" or ident = "KCHO" or ident = "KCSG" or ident = "KGRI" or
                       ident = "KLCH" or ident = "KPTK" or ident = "KPVU";"""
        cursor = config.conn.cursor(dictionary=True)
        cursor.execute(sql3)
        result = cursor.fetchall()
        all_airports = result

        # Format data to dictionary
        response_dict = {"all_airports_data": all_airports, "start_airport_data": start_airport_data, "status": self.status}

        # Insert the newly created game into the database
        sql2 = "INSERT INTO Game (id, location, player_range, screen_name) VALUES (%s, %s, %s, %s)"
        cursor = config.conn.cursor()
        cursor.execute(sql2, (self.status["id"], self.status["location"], self.status["battery_range"], self.status["player_name"]))
        config.conn.commit()
        print(f"this is self.status values: {self.status}")

        return response_dict