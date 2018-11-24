import os
import requests

default_secrets_path = os.path.join(os.environ['HOME'],
                                    '.secrets/opendota_api_key')

def get_api_key(filename: str=default_secrets_path) -> str:
    """Load OpenDota api key."""
    with open(filename) as f:
        api_key = f.read().strip()
        return api_key

api_key = get_api_key()

def get_match_data(match_id: int, api_key: str=api_key) -> dict:
    """Retrieve data for specfied match from the OpenDota api."""
    url = 'https://api.opendota.com/api/matches/271145478'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    return response.json()
