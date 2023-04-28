import config
import os
import requests

from dotenv import load_dotenv
load_dotenv()


"""
#get goal number from a API
goal_api = requests.get('http://www.randomnumberapi.com/api/v1.0/random?min=0&max=5&count=1')
goal_json = goal_api.json()

airports = []
for row in res:

    airports.append({
        "name": row[0],
        "ident": row[1],
        "goal": None,
        "latitude": row[2],
        "longitude": row[3],
        "type": row[4],
    })
return airports
"""