from aptly_api import routes
from config import APTLY_URL

import requests
import os 

API_USER = os.environ.get('API_USER')
API_PASS = os.environ.get('API_PASSWORD')
GPG_PASSPHRASE = os.environ.get('GPG_PASSPHRASE')


def repo_show(repo_name):
    response = requests.get('{}{}{}'.format(APTLY_URL, routes["repo"], repo_name), auth=(API_USER, API_PASS))
    repo_data = response.text
    return repo_data

