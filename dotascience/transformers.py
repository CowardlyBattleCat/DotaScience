# TODO finish and fix type annotations

from typing import List, Dict, Any


def get_match_ids(pro_match_data: List[dict]) -> List[int]:
    """Consume list of pro match stubs. Return list of match ids."""
    match_ids = []
    for match in pro_match_data:
        match_ids.append(match['match_id'])
    return match_ids

def get_patch(match: Dict) -> Tuple[int]:
    """Consume data for a match. Return (match_id, patch)"""
    return (match['match_id'], match['patch'])

def filter_by_patch(bulk_match_data: List[Dict],
                    min_patch: int=35, max_patch: int=38) -> List[Dict]:
    """Return list of match data having patch in specfied range (inclusive).
    patch key:
    OpenDota patch value -> Dota 2 patch
    34 -> 7.15
    35 -> 7.16
    36 -> 7.17
    37 -> 7.18
    38 -> 7.19
    39 -> 7.20
    """
    filtered_matches = []
    for match in bulk_match_data:
        match_patch = get_patch(match)[1]
        if (match_patch >= min_patch and match_patch <= max_patch):
            filtered_matches.append(match)
    return filtered_matches
