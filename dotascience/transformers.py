from typing import List, Dict, Any


def get_match_ids(pro_match_data: List[dict]) -> List[int]:
    """Return list of match ids from list of pro match stubs."""
    match_ids = []
    for match in pro_match_data:
        match_ids.append(match['match_id'])
    return match_ids
