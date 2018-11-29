import os
import requests
from typing import List, Dict, Any

default_secrets_path = os.path.join(os.environ['HOME'],
                                    '.secrets/opendota_api_key')

def get_api_key(filename: str=default_secrets_path) -> str:
    """Load OpenDota api key."""
    with open(filename) as f:
        api_key = f.read().strip()
        return api_key

api_key = get_api_key()

def get_hero_data(api_key: str=api_key) -> List[dict]:
    """Retrieve data for heroes from the OpenDota api."""
    url = 'https://api.opendota.com/api/heroes'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    return response.json()

def get_pro_match_stubs(less_than_match_id: int,
                        api_key: str=api_key) -> List[dict]:
    """Retrieve data stubs for pro matches with match ids smaller than
    less_than_match_id from the OpenDota api. The api seems to return 100 stubs
    at a time by default.
    """
    url = 'https://api.opendota.com/api/proMatches'
    params = {'api_key': api_key, 'less_than_match_id': less_than_match_id}
    response = requests.get(url, params=params)
    return response.json()

def accumulate_pro_match_stubs(less_than_match_id: int, end_match_id: int,
                               api_key: str=api_key) -> List[dict]:
    """Call get_pro_match_stubs repeatedly and combine results until the last
    match_id returned is smaller than end_match_id.
    """
    pro_match_stubs = []
    lowest_match_id = less_than_match_id
    while lowest_match_id >= end_match_id:
        stubs = get_pro_match_stubs(lowest_match_id, api_key)
        pro_match_stubs.extend(stubs)
        lowest_match_id = stubs[-1]['match_id']
    return pro_match_stubs

def get_match_data(match_id: int, api_key: str=api_key) -> dict:
    """Retrieve data for specfied match from the OpenDota api."""
    url = 'https://api.opendota.com/api/matches/' + str(match_id)
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    return response.json()

def get_bulk_match_data(match_ids: List[int]) -> List[dict]:
    bulk_match_data = []
    for match_id in match_ids:
        bulk_match_data.append(get_match_data(match_id))
        print(match_id)
    return bulk_match_data
