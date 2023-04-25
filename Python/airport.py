import config
import os
import requests

from dotenv import load_dotenv
load_dotenv()
from geopy import distance

class Airport:
    def __init__(self, ident, name, latitude_deg, longitude_deg, type, weather_description, weather_degrees):
        self.ident = ident
        self.name = name
        self.latitude_deg = latitude_deg
        self.longitude_deg = longitude_deg
        self.type = type
        self.weather_description = weather_description
        self.weather_degrees = weather_degrees

    def get_airports(self):
        sql = """SELECT name, ident, latitude_deg, longitude_deg, type FROM airport
            WHERE ident = "KLAX" or ident = "KJFK" or ident = "KAUS" or ident = "KMSP" or ident = "KSEA" or ident = "KABQ" or ident = "KALN" or 
            ident = "KBIL" or ident = "KBIS" or ident = "KCHO" or ident = "KCSG" or ident = "KGRI" or
            ident = "KLCH" or ident = "KPTK" or ident = "KPVU";;"""
        cur = config.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()

        airports = []
        for row in res:

            airports.append({
                "name": row[0],
                "ident": row[1],
                "latitude": row[2],
                "longitude": row[3],
                "type": row[4],
                "weather": get_airport_weather(row[2], row[3])
            })
        return airports


def get_airport_weather(latitude, longitude):
    apikey = os.environ.get('API_KEY')
    request = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=" + apikey + "&units=metric"
    response = requests.get(request).json()
    weather_description = response['weather'][0]['description']
    weather_temp = response['main']['temp']
    return weather_description, weather_temp

