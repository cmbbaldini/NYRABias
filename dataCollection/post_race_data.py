import json
import requests

def postRace(data):
    url = 'https://nyra-bias.onrender.com/post/'
    data = json.dumps(data)
    headers = {'Content-type': 'application/json', "Authorization": "Token MyToken"}
    r = requests.post(url, data=data, headers=headers)
    print(r.content)