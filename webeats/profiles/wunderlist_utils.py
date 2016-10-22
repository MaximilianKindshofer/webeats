from .secret import client_id, client_secret
import json
import requests

def get_authorization_url(client_id, redirect_url, state):
    return "https://www.wunderlist.com/oauth/authorize?client_id={}&redirect_uri={}&state={}".format(client_id, redirect_url, state)

def make_api_call(code):

    post_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            }

    wunderlist_token_url = 'https://www.wunderlist.com/oauth/access_token'
    r = requests.post(wunderlist_token_url, data=post_data)
    json_response = r.json()
    response = json.loads(json_response)
    token = response['access_token']
    return token
