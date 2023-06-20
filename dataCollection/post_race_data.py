import json
import requests

def postRace(data):
    url = 'https://nyra-bias.onrender.com/post/'
    data = json.dumps(data)
    headers = {'Content-type': 'application/json', "Authorization": "Token 9e8347a90c0772afd666140e45233fd7bbd995d2"}
    r = requests.post(url, data=data, headers=headers)
    print(r.content)