"""
helpers.py


"""

from typing import List, Tuple, Optional

episode_counts = [6, 22, 23, 14, 26, 24, 24, 24, 23]


def check_validity(season: int, episode: int):
    """Shorthand function for checking if a specific episode is valid."""
    return (1 <= season <= 9) and (1 <= episode <= episode_counts[season])


def default(value, other):
    """Value default, similar to dict.get, but better."""
    return value if value is not None else other


def get_neighbors(array: List, index: int, distance: int = 2) -> Tuple[List, List]:
    """Get neighbors above and below a specific index in an array. Returns maximum number of items possible."""
    top, below = [], []
    for i in range(1, distance + 1):
        top_index = index - i
        below_index = index + i
        if top_index >= 0:
            top.append(array[top_index])
        if below_index < len(array):
            below.append(array[below_index])
    return top[::-1], below


def algolia_transform(old_dictionary: dict, key_list: List[Tuple[str, Optional[str]]]) -> dict:
    """
    Transforms a dictionary object of a quote (from algolia.json) into a API-ready quote.
    Used for cli.character (i.e. characters.json)
    :param old_dictionary: The original Algolia dictionary
    :param key_list: A list of keys to keep in the dictionary in a tuple. One item tuple to keep the tuple's name, a
    second item requests a 'rename' for the quote.
    :return: The reformatted dictionary.
    """

    new_dictionary = {}
    for keyItem in key_list:
        if len(keyItem) > 1:
            new_dictionary[keyItem[1]] = old_dictionary[keyItem[0]]
        else:
            new_dictionary[keyItem[0]] = old_dictionary[keyItem[0]]

    return new_dictionary


def is_main_character(name: str) -> bool:
    return None

def character_id(name: str) -> str:
    return '-'.join(name.split(' ')).lower()
