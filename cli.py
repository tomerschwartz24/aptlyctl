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

def show_repo_packages(repo_name, package_name="", details=False, with_deps=False):
    query_specific_pkg = f"?q={package_name}"
    if details:
        format_pkg_details = "format=details"
    else:
        format_pkg_details = ""
    
    if with_deps:
        describe_pkg_deps = "withDeps=1"
    else:
        describe_pkg_deps = "withDeps=0"
        
    try:
        response = requests.get('{}{}{}/packages{}&{}&{}'.format(APTLY_URL, routes["repo"], repo_name, query_specific_pkg, format_pkg_details, describe_pkg_deps), auth=(API_USER, API_PASS))
        response.raise_for_status()
        repo_packages = response.json()
        for pkg in repo_packages:
            print(json.dumps(pkg, indent=4))
            

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

def delete_repo(repo_name, force):
    #Fix deleting repositories with symbols (not working) (such as @@@#)

    try:
        
        response = requests.delete("{}{}{}?force={}".format(APTLY_URL, routes["repo"], repo_name, force), auth=(API_USER, API_PASS))
        response.raise_for_status()
        return f"{repo_name} repository has been deleted!"
        
    except requests.exceptions.HTTPError as error:
        return f"{error} \n {response.content}"

def upload_single_file_to_aptly_upload_dir(repo_name, filepath):
    try:
        file = {'file': open(filepath, 'rb')}
        #Add validation that upload file is actually deb file
        response = requests.post('{}{}{}'.format(APTLY_URL, routes["file"], repo_name), auth=(API_USER, API_PASS), files=file)
        response.raise_for_status()
        print(response.text)
    except FileNotFoundError as nofile_error :
        print(nofile_error)
    
    except requests.exceptions.HTTPError as error:
        print(error)

def upload_entire_deb_folder_to_upload_dir(repo_name, local_deb_dir):
    try:
        list_of_debs_to_upload = [os.path.join(local_deb_dir, file) for file in os.listdir(local_deb_dir)]
        for deb_file in list_of_debs_to_upload:
            #Add validation that upload file is actually deb file, only omit files that aren't deb file
            file_to_upload = {'file': open(deb_file, 'rb')}
            response = requests.post('{}{}{}'.format(APTLY_URL, routes["file"], repo_name), auth=(API_USER, API_PASS), files=file_to_upload)
            response.raise_for_status()
            print(response.text)
    except FileNotFoundError as nofile_error :
        print(nofile_error)
    
    except requests.exceptions.HTTPError as error:
        print(error)
