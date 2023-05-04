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
def all_airports_in_range(current_ident, a_ports, player_range):
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


# get airports in range
def medium_airports_in_range(current_ident, a_ports, player_range):
    mediums_in_range = []
    all_airports_list = all_airports_in_range(current_ident,a_ports,player_range)
    for a_port in all_airports_list:
        if a_port['type'] == 'medium_airport':
            mediums_in_range.append(a_port)
    return mediums_in_range


# Query to get all airports with matching goals
def get_airports(game_id):
    sql = f"""SELECT a.name, a.ident, a.type, a.latitude_deg, a.longitude_deg, p.game, p.goal, p.opened FROM airport a
                JOIN ports p ON a.ident = p.airport WHERE p.game = '{game_id}';"""
    cur = config.conn.cursor(dictionary=True)
    cur.execute(sql)
    res = cur.fetchall()
    res.append
    return res


def check_goal(game_id, dest):
    sql = f"select goal, opened from ports where game={game_id} and airport='{dest}'"
    cur = config.conn.cursor(dictionary=True)
    cur.execute(sql)
    res = cur.fetchall()
    return res


def update_ports_table(game_id, dest):
    sql = f"UPDATE ports SET opened = 1 WHERE game = {game_id} AND airport = '{dest}'"
    cursor = config.conn.cursor()
    cursor.execute(sql)
    config.conn.commit()


def update_game_table(game_id, dest, player_range):
    sql = f"UPDATE game SET location = '{dest}', player_range = {player_range} WHERE id={game_id}"
    cursor = config.conn.cursor()
    cursor.execute(sql)
    config.conn.commit()


class Game:
    def __init__(self, game_id):
        # Game_id comes from the URL
        self.game_id = game_id
        self.current_ident = get_player_data(self.game_id)[0]['location']
        config.player_name = get_player_data(self.game_id)[0]['screen_name']
        self.current_airport = get_airport_info(self.current_ident)[0]
        self.all_airports = get_airports(self.game_id)

        # Placeholder text for the HTML element - This text is displayed when a new game is started
        self.event = "Welcome to the last of the USA! This box is here to keep you updated on the game events. " \
                     "It will automatically update during the game"

        self.status = {
            "id": self.game_id,
            "name": config.player_name,
            "food_collected": config.food,
            "water_collected": config.water,
            "solar_collected": config.solar,
            "medicine_collected": config.medicine,
            "battery_range": get_player_data(self.game_id)[0]['player_range'],
            "event": self.event
        }

    def what_goal_in_airport(self, game_id, dest):
        goal_at_current = check_goal(game_id, dest)[0]['goal']

        if goal_at_current == 0:
            self.status['food_collected'] = True
            self.status['event'] = "You found the food resources you needed!"

        elif goal_at_current == 1:
            self.status['water_collected'] = True
            self.status['event'] = "You found the water purification resources you needed!"

        elif goal_at_current == 2:
            self.status['solar_collected'] = True
            self.status['event'] = "You found the necessary solar panels!"

        elif goal_at_current == 3:
            self.status['medicine_collected'] = True
            self.status['event'] = "You found the medical supplies you needed!"

        elif goal_at_current == 4:
            self.status['event'] = 'You searched through the whole airport but came out empty handed.'

        elif goal_at_current == 5:
            self.status['event'] = 'You faced a robber with bad intentions but made it out just in the nick of time.' \
                         ' Unfortunately empty handed. '

    def check_airports_in_range(self):
        self.airports_in_range = all_airports_in_range(self.current_ident, self.all_airports, self.status['battery_range'])
        self.all_game_data = {
            'all_airports': self.airports_in_range,
            'current_airport': self.current_airport,
            'status': self.status}
        return self.all_game_data

    def fly(self, game_id, dest, dist, day):

        # travel distance is subtracted from battery range
        self.status['battery_range'] -= float(dist)/2

        # Check what goal does this destination airport contain and update the player
        self.what_goal_in_airport(game_id, dest)

        # Update player data on new location
        self.game_id = game_id
        self.current_ident = get_player_data(game_id)[0]['location']
        self.current_airport = get_airport_info(self.current_ident)[0]

        # Update database
        update_ports_table(self.game_id, dest)
        update_game_table(self.game_id, dest, self.status['battery_range'])

        # If this new airport is a large airport player gets more range by charging their plane
        if get_airport_info(dest)[0]['type'] == 'large_airport':
            self.status['battery_range'] += 1500
            self.status['event'] += ". During your searching you charged your plane and got more range to play with!"

        # Define the ident code of the airport to remove from all airports.
        ident_to_remove = dest

        # Iterate through the list and remove the element with matching ident code
        for i in range(len(self.all_airports)):
            if self.all_airports[i]["ident"] == ident_to_remove:
                self.all_airports.pop(i)
                break

        # Through the URL "day" variable determine did player choose: 1 large airport per day or 2 mediums per day
        if day.isdigit():
            # This is the path if player chose 1 large airport or already explored 1 medium
            # meaning they get to see both types of airports in their next choice
            return self.check_airports_in_range()

        else:
            # This path is active when player chooses to explore 2 medium airports in a day
            # Therefore this path only returns mediums of which the player can choose their next destination

            self.mediums_in_range = medium_airports_in_range(self.current_ident, self.all_airports, self.status['battery_range'])
            self.half_day_data = {
                'all_airports': self.mediums_in_range,
                'current_airport': self.current_airport,
                'status': self.status}
            return self.half_day_data
