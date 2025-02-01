from aptly_api import routes
from config import APTLY_URL

import requests
import json
import os 

API_USER = os.environ.get('API_USER')
API_PASS = os.environ.get('API_PASS')
GPG_PASSPHRASE = os.environ.get('GPG_PASSPHRASE')


def list_repos():
    try:
        response = requests.get('{}{}'.format(APTLY_URL, routes["repo"]), auth=(API_USER, API_PASS))
        response.raise_for_status()
        repo_list_of_dicts = response.json()
        for repo in repo_list_of_dicts:
            print(json.dumps(repo, indent=4))

    except requests.exceptions.HTTPError as error:
        return error

def show_repo(repo_name):
    try:
        response = requests.get('{}{}{}'.format(APTLY_URL, routes["repo"], repo_name), auth=(API_USER, API_PASS))
        response.raise_for_status()
        repo_data = response.text
        return repo_data
    except requests.exceptions.HTTPError as error:
        return error

def create_repo(repo_name, comment="", default_distribution="", default_component="", from_snapshot=""):               
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
    
def upload_single_file_to_aptly(repo_name, filepath):
    try:
        file = {'file': open(filepath, 'rb')}
        response = requests.post('{}{}{}'.format(APTLY_URL, routes["file"], repo_name), auth=(API_USER, API_PASS), files=file)
        response.raise_for_status()
        print(response.text)
    except FileNotFoundError as nofile_error :
        print(nofile_error)
    
    except requests.exceptions.HTTPError as error:
        print(error)
