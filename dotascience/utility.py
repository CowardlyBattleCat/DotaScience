# TODO finish and fix type annotations

import csv
import json
from typing import List, Dict, Any, Optional

def save_as_csv(data: List[int], filename_path: str):
    """Save data as a .csv file of integers using the given filename path,
    adding .csv to end of file if needed.
    """
    if filename_path[-4:] != '.csv':
        filename_path += '.csv'
    with open(filename_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([data])

def load_csv(filename_path: str) -> List:
    """Load .csv file of integers as a list of integers using specfied path."""
    with open(filename_path, newline='') as f:
        reader = csv.reader(f)
        csv_list = []
        for row in reader:
            row = [int(x) for x in row]
            csv_list.extend(row)
        return csv_list

def save_as_json(data, filename_path: str):
    """Save data as a .json file using the given filename path, adding .json
    to end of file if needed.
    """
    if filename_path[-5:] != '.json':
        filename_path += '.json'
    with open(filename_path, 'w') as outfile:
        json.dump(data, outfile)

def load_json(filename_path: str):
    """Load .json from specified filename path."""
    with open(filename_path) as infile:
        return json.load(infile)

def find_index(match_list: List[int], match_id: int):
    """Consume a list of matches and a specific match id. Return index for
    match id.
    """
    for i, match in enumerate(match_list):
        if match == match_id:
            return (i, match)
