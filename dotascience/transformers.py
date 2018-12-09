# TODO finish and fix type annotations

import pandas as pd
import numpy as np
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
    """Return a list of unique levels present in lists from a given column.
    Called by make_list_dummies.
    """
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
    Called by make_list_dummies.
    """
    if type(column) != list:
        return 0
    elif level in column:
        return 1
    else:
        return 0

def clean_df(df, column: str):
    """Drop original column from df with newly created dummy columns.
    Called by make_list_dummies.
    """
    return df.drop(labels=column, axis=1)

def make_list_dummies(df, column: str):
    """Consume a dataframe and categorical column with lists of levels as row
    values.
    Return a dataframe with each unique level as its own dummy variable.
    Dummy column names have original column name separated from level names
    with __ (double underscore) and spaces in level names replaced with _
    (single underscore).
    """
    dummies_df = pd.DataFrame(df[column].copy())
    for level in make_unique_list(dummies_df[column]):
        new_col_name = f'{column}__{level.replace(" ", "_")}'
        dummies_df[new_col_name] = dummies_df[column].apply(
            lambda col: is_level_in_col(col, level))
    dummies_df = clean_df(df=dummies_df, column=column)
    return dummies_df

def merge_hero_dummies(main_df, dummy_dfs, cols_to_drop=None):
    """Consume a main df, a list of dummy dfs, and a list of columns to drop.
    Return a single df inner merged on left index and right index and missing
    the specified columns.
    """
    builder_df = main_df.copy()
    for df in dummy_dfs:
        builder_df = pd.merge(left=builder_df, right=df,
                              left_index=True, right_index=True)
    if cols_to_drop is not None:
        builder_df.drop(columns=cols_to_drop, inplace=True)
    return builder_df

def sum_rows_with_nulls(match_df):
    """Consume a dataframe of matches and return columns with nulls and how
    many null rows are in each column.
    """
    null_columns = match_df.columns[match_df.isnull().any()]
    return match_df[null_columns].isnull().sum()

def remove_rows_with_nulls(match_df, cols_with_nuls):
    """Consume a dataframe of matches and a list of columns having null rows.
    Return a new data frame having dropped null rows from those columns.
    """
    dropped_nulls_match_df = match_df.copy()
    for col in cols_with_nuls:
        dropped_nulls_match_df = dropped_nulls_match_df[
            ~dropped_nulls_match_df[col].isnull()]
    return dropped_nulls_match_df

def make_hero_pick_ban_col_names(full_hero_data_df) -> List[str]:
    """Consume a dataframe of hero data. Return a list of strings with
    specified pick and ban hero columns for each side.
    """
    draft_steps = ['pick', 'ban']
    hero_ids = list(full_hero_data_df.index.values)
    hero_pick_ban_col_names = []
    sides = ['radiant', 'dire']
    for step in draft_steps:
        for side in sides:
            for hero_id in hero_ids:
                side_hero_choice = f'{side}_{step}__{hero_id}'
                hero_pick_ban_col_names.append(side_hero_choice)
    return hero_pick_ban_col_names

def add_new_zero_cols(match_data_df, col_names):
    """Consume a dataframe of match data and a list of column names.
    Return a new dataframe with columns of zeroes for each col in col_names.
    """
    n_rows = len(match_data_df)
    n_cols = len(col_names)
    zero_array = np.zeros(shape=(n_rows, n_cols), dtype=int)
    empty_df = pd.DataFrame(zero_array, index=match_data_df.index, columns=col_names)
    extended_match_df = pd.merge(match_data_df, empty_df, left_index=True, right_index=True)
    return extended_match_df

def assign_picks_bans(one_match):
    """Consume one match with empty pick and ban columns.
    Return match with populated columns.
    """
    for pick_ban in one_match['picks_bans']:
        if pick_ban['is_pick']:
            hero_id = pick_ban['hero_id']
            if pick_ban['team'] == 0:
                one_match[f'radiant_pick__{hero_id}'] = 1
            else:
                one_match[f'dire_pick__{hero_id}'] = 1
        elif pick_ban['is_pick'] == False:
            hero_id = pick_ban['hero_id']
            if pick_ban['team'] == 0:
                one_match[f'radiant_ban__{hero_id}'] = 1
            else:
                one_match[f'dire_ban__{hero_id}'] = 1
    return one_match

def create_hero_pick_ban_dummies(match_data_df, col_names):
    """Consume a dataframe of matches with draft data and target label.
    Return a new dataframe with a dummy column for each of the 464
    combinations of side + pick + pick/ban.
    """
    new_df = add_new_zero_cols(match_data_df, col_names)
    for match in match_data_df.index:
        row = new_df.loc[match].copy()
        new_df.loc[match] = assign_picks_bans(row)
    new_df.drop(columns='picks_bans', inplace=True)
    return new_df

def make_hero_category_col_names(hero_categories: List[str]) -> List[str]:
        hero_category_col_names = []
        sides = ['radiant', 'dire']
        for side in sides:
            for hero_category in hero_categories:
                side_category_num = f'{side}_heroes__{hero_category}'
                hero_category_col_names.append(side_category_num)
        return hero_category_col_names
