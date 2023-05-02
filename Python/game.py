import config
from geopy import distance


def get_player_data(game_id):
    sql = f"select * from game where id='{game_id}'"
    cursor = config.conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_player_goals(game_id):
    sql = f"select airport,goal,opened from ports where game='{game_id}'"
    cursor = config.conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_airport_info(ident):
    sql = f"select name,ident,latitude_deg,longitude_deg,type from airport where ident='{ident}'"
    cursor = config.conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def calculate_distance(current, destination):
    first = get_airport_info(current)
    second = get_airport_info(destination)
    return distance.distance((first[0]['latitude_deg'], first[0]['longitude_deg']),
                             (second[0]['latitude_deg'], second[0]['longitude_deg'])).km


# get airports in range
def airports_in_range(current_ident, a_ports, player_range):
    in_range = []
    for a_port in a_ports:
        distance_between = calculate_distance(current_ident, a_port['ident'])
        if distance_between <= player_range and not distance_between == 0:
            a_port['in_range'] = True
        else:
            a_port['in_range'] = False
        a_port['active'] = False
        a_port['goal_opened'] = False
        a_port['distance_to'] = round(distance_between, 2)
        in_range.append(a_port)
    return in_range


# Query to get all airports with matching goals
def get_airports(game_id):
    sql = f"""SELECT a.name, a.ident, a.type, a.latitude_deg, a.longitude_deg, p.game, p.goal, p.opened FROM airport a
                JOIN ports p ON a.ident = p.airport WHERE p.game = '{game_id}';"""
    cur = config.conn.cursor(dictionary=True)
    cur.execute(sql)
    res = cur.fetchall()
    return res

def check_goal(game_id, ident):
    sql = f"SELECT goal FROM ports WHERE "
    cur = config.conn.cursor(dictionary=True)
    cur.execute(sql)
    res = cur.fetchall()
    return res


class Game:
    def __init__(self, game_id):
        # Game_id comes from the URL
        self.game_id = game_id
        self.current_ident = get_player_data(self.game_id)[0]['location']
        config.player_name = get_player_data(self.game_id)[0]['screen_name']
        config.battery = get_player_data(self.game_id)[0]['player_range']
        self.current_airport = get_airport_info(self.current_ident)[0]
        self.all_airports = get_airports(self.game_id)


        self.status = {
            "id": self.game_id,
            "name": config.player_name,
            "food_collected": config.food,
            "water_collected": config.water,
            "solar_collected": config.solar,
            "medicine_collected": config.medicine,
            "battery_range": config.battery,
            "days_left": config.days_left
        }

    def fly(self, game_id, dest, dist):
        # TODO distancen vähennys
        self.game_id = game_id
        self.current_ident = get_player_data(game_id)[0]['location']
        self.current_airport = get_airport_info(self.current_ident)[0]

        sql = f"UPDATE ports SET opened = 1 WHERE game = {self.game_id} AND airport = '{dest}'"
        cursor = config.conn.cursor()
        cursor.execute(sql)

        sql = f"UPDATE game SET location = '{dest}', player_range = {config.battery} WHERE id={self.game_id}"
        cursor = config.conn.cursor()
        cursor.execute(sql)
        config.conn.commit()

        # Define the ident code of the airport to remove from all airports.
        ident_to_remove = dest

        # Iterate through the list and remove the element with matching ident code
        for i in range(len(self.all_airports)):
            if self.all_airports[i]["ident"] == ident_to_remove:
                self.all_airports.pop(i)
                break

        return self.check_airports_in_range()

    def check_airports_in_range(self):
        self.airports_in_range = airports_in_range(self.current_ident, self.all_airports, config.battery)
        self.all_game_data = {
            'all_airports': self.airports_in_range,
            'current_airport': self.current_airport,
            'status': self.status}

        return self.all_game_data

