# TODO finish and fix type annotations

from typing import List, Dict, Any, Tuple


# Functions for use with .json objects
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


# Functions for use with Pandas objects
def make_unique_list(column):
    """Return a list of unique levels present in lists from a given column."""
    unique_levels=[]
    for item in column:
        if type(item)==list:
            for level in item:
                if level not in unique_levels:
                    unique_levels.append(level)
    unique_levels.sort()
    return unique_levels

def is_level_in_col(column, level):
    """For a single row:
    Return 1 if the level is present in the column.
    Return 0 if the level is not present in the column.
    """
    if type(column) != list:
        return 0
    elif level in column:
        return 1
    else:
        return 0

def clean_df(df, column: str):
    """"""
    return df.drop(labels=column, axis=1)

def make_list_dummies(df, column: str):
    dummies_df = pd.DataFrame(df[column].copy())
    for level in make_unique_list(dummies_df[column]):
        dummies_df[f'{column}_{level.replace(" ", "-")}'] = dummies_df[column].apply(
            lambda col: is_level_in_col(col, level)
        )
    dummies_df = clean_df(df=dummies_df, column=column)
    return dummies_df
