from aptly_api import routes
from config import APTLY_URL

import requests
import os 

API_USER = os.environ.get('API_USER')
API_PASS = os.environ.get('API_PASS')
GPG_PASSPHRASE = os.environ.get('GPG_PASSPHRASE')


def repo_show(repo_name):
    # import ipdb
    # ipdb.set_trace()
    try:
        response = requests.get('{}{}{}'.format(APTLY_URL, routes["repo"], repo_name), auth=(API_USER, API_PASS))
        response.raise_for_status()
        repo_data = response.text
        return repo_data

    except requests.exceptions.HTTPError as error:
        return error
