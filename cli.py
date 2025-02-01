from aptly_api import routes
from config import APTLY_URL

import requests
import os 

API_USER = os.environ.get('API_USER')
API_PASS = os.environ.get('API_PASS')
GPG_PASSPHRASE = os.environ.get('GPG_PASSPHRASE')


def repo_show(repo_name):
    try:
        response = requests.get('{}{}{}'.format(APTLY_URL, routes["repo"], repo_name), auth=(API_USER, API_PASS))
        response.raise_for_status()
        repo_data = response.text
        return repo_data
    except requests.exceptions.HTTPError as error:
        return error

def repo_create(repo_name, comment="", default_distribution="", default_component="", from_snapshot=""):               
    repo_creation_data = {"Name": repo_name, 
                          "Comment": comment, 
                          "DefaultDistribution": default_distribution,
                          "DefaultComponent": default_component,
                          "FromSnapshot": from_snapshot }
    try:
        response = requests.post('{}{}'.format(APTLY_URL, routes["repo"]), auth=(API_USER, API_PASS), data=repo_creation_data)
        response.raise_for_status()
        repo_data = response.text
        return f"Repository has been created successfully!\n{repo_data}"
    

    
    except requests.exceptions.HTTPError as error:
        if "409" in str(error):
            print(f"Unable to create repository {repo_name}, most likely already exist!")
        return error
    

