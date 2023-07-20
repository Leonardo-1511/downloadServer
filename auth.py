import requests as rq
import json
import os

auth_url = f"https://www.dropbox.com/oauth2/authorize?client_id={os.environ['client_id']}&redirect_uri={rq.utils.quote('https://yetanotherapiimplementation.leonardo1511.repl.co/callback', safe='')}&response_type=code&state=dropbox_oauth_flow"

def authorize():
    request = auth_url
    return request
    