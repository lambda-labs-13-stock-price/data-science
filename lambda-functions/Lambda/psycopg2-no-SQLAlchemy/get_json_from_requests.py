import requests

def get_items():
    '''
    Get JSON objects from flask API endpoint
    '''
    # this link can change or be changed to be dynamic
    endpoint = 'https://intense-bastion-55085.herokuapp.com/data'

    r = requests.get(endpoint)

    return r.json()
