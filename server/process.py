"""
process.py

Functions and shortcuts for loading/saving/extracting data for processing quote data.
"""

import json
import os
import time
from collections import defaultdict
from math import ceil
from typing import Dict, Iterable, List, Optional, Tuple, Union

import enlighten
import requests

session = requests.Session()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

folder_exts = {'html': 'html', 'processed': 'json', 'raw': 'txt'}
episode_counts = [6, 22, 23, 14, 26, 24, 24, 24, 23]


def get_filename(season: int, episode: int, extension: str) -> str:
    """Get filename for any given episode in standardized format"""
    return f'{season}-{str(episode).zfill(2)}.{extension}'


def get_filepath(season: int, episode: int, folder: str) -> str:
    """Get full filepath for a episode's datafile for a given folder."""
    if folder:
        return os.path.join(DATA_DIR, folder, get_filename(season, episode, folder_exts.get(folder, 'json')))
    return os.path.join(DATA_DIR, get_filename(season, episode, 'json'))


def load_file(filepath: str, json_decode: bool = False):
    """Shortcut function for loading file from filepath, with JSON parsing flag."""
    if json_decode:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()


def save_file(filepath: str, data, json_encode: bool):
    """Shortcut function for saving data to a file, JSON encoding flag."""
    if json_encode:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    else:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(data)


def get_episodes(season: int = None) -> Iterable[Tuple[int, int]]:
    """
    Yields a list of Episode & Season tuples.
    If Season is specified, it yields
    """
    if season:
        if 1 <= season <= 9:
            for episode in range(1, episode_counts[season - 1]):
                yield season, episode
    else:
        for season, ep_count in enumerate(episode_counts, start=1):
            for episode in range(1, ep_count + 1):
                yield season, episode


def verify_episode(season: int, episode: int = None) -> bool:
    """
    Verifies that specific Season and/or Episode is valid.
    """
    return 1 <= season <= 9 and (episode is None or 1 <= episode <= episode_counts[season])


def sleep_from(wait_time: float, moment: float, manager: enlighten.Manager = None) -> float:
    """
    Sleeps for a specific amount of time, accordingly to a previous moment.

    :param wait_time: The minimum amount of time that must be waited since the specified moment.
    :param moment: Epoch time.
    :param manager: Progressbar Manager
    """
    passed = time.time() - moment
    time_slept = wait_time - passed
    if time_slept > 0.01:
        if manager:
            time_slept = round(time_slept, 2)
            total, delay = ceil(time_slept * 100), time_slept / 100
            bar = manager.counter(total=total, desc='Sleeping...', leave=False)
            for _ in range(total):
                time.sleep(delay)
                bar.update()
            bar.close()
        else:
            time.sleep(time_slept)
        return time_slept
    else:
        return 0


def get_appearances(season, episode) -> Optional[List[Dict[str, Union[int, str]]]]:
    """
    Extracts all characters and their number of appearances from a specific episode.
    Prepared in a list of dictionary, preferable storage/for loop method.
    """
    filepath = get_filepath(season, episode, 'processed')
    if not os.path.exists(filepath):
        return
    scenes = load_file(filepath, True)

    characters = defaultdict(int)
    for scene in scenes:
        for quote in scene.get('quotes', []):
            characters[quote.get('speaker')] += 1
    characters = [{'name': character, 'appearances': appearances, 'id': character_id(character)}
                  for character, appearances in characters.items()]
    return list(sorted(characters, key=lambda item: item['appearances'], reverse=True))
