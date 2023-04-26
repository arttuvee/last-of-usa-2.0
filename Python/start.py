import config
import random

class Start:
    def __init__(self):
        self.all_airports = self.get_airports()
        self.start_airport = self.starting_airport()
        self.final_airport = self.final_airport()

    def starting_airport(self):
        sql = ' select * from airport where iso_country = "US" and type = "small_airport" and longitude_deg > -125 order by rand() limit 1;'
        cursor = config.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def get_airports(self):
        sql = """SELECT name, ident, latitude_deg, longitude_deg, type FROM airport
                       WHERE ident = "KLAX" or ident = "KJFK" or ident = "KAUS" or ident = "KMSP" or ident = "KSEA" or ident = "KABQ" or ident = "KALN" or 
                       ident = "KBIL" or ident = "KBIS" or ident = "KCHO" or ident = "KCSG" or ident = "KGRI" or
                       ident = "KLCH" or ident = "KPTK" or ident = "KPVU";;"""
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

    def create_game(self,location, screen_name, player_range, a_ports):
        # Inserts the values to the new game session
        sql = " INSERT INTO game (location, screen_name, player_range) VALUES (%s, %s, %s);"
        cursor = config.conn.cursor()
        cursor.execute(sql, (location, screen_name, player_range))
        game_id = cursor.lastrowid

        goals = self.get_goals()
        goal_list = []
        for goal in goals:
            for i in range(0, goal["probability"], 1):
                goal_list.append(goal["id"])

        # Brings all the airports to the started game session
        goal_airports = a_ports.copy()
        random.shuffle(goal_airports)

        for i, goal_id in enumerate(goal_list):
            sql = "INSERT INTO ports (game, airport, goal) VALUES (%s, %s, %s);"
            cursor = config.conn.cursor()
            cursor.execute(sql, (game_id, goal_airports[i]['ident'], goal_id))
        return game_id

