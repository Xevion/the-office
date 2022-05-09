"""
helpers.py


"""
import random
import re
import string
import unicodedata
from collections import OrderedDict
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest
from typing import List, Optional, Tuple

import unidecode

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


alphabet: str = string.ascii_letters + string.digits


def random_id(length: int = 8) -> str:
    """Generate a random {length} character long string."""
    return ''.join(random.choices(alphabet, k=length))


def char_filter(string):
    latin = re.compile('[a-zA-Z]+')
    for char in unicodedata.normalize('NFC', string):
        decoded = unidecode.unidecode(char)
        if latin.match(decoded):
            yield char
        else:
            yield decoded


def clean_string(string):
    return "".join(char_filter(string))


def get_close_matches_indexes(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return a list of the indexes of the best
    "good enough" matches. word is a sequence for which close matches
    are desired (typically a string).
    possibilities is a list of sequences against which to match word
    (typically a list of strings).
    Optional arg n (default 3) is the maximum number of close matches to
    return.  n must be > 0.
    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.
    """

    if not n > 0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
                s.quick_ratio() >= cutoff and \
                s.ratio() >= cutoff:
            result.append((s.ratio(), idx))

    # Move the best scorers to head of list
    result = _nlargest(n, result)

    # Strip scores for the best n matches
    return [x for score, x in result]


def marked_item_merge(keys: List[str], values: List[int]) -> Tuple[List[str], List[str]]:
    """Add the values of identical keys together, then return both the keys and values"""
    merge = OrderedDict()
    for key, value in zip(keys, values):
        # Already inserted, now make/keep it negative
        if key in merge.keys():
            # Keys that haven't been turned over need to be made negative
            if merge[key] > 0:
                merge[key] = -merge[key]

            # And then subtract the value in all cases
            merge[key] -= value
        else:
            # Values that are positive didn't merge with other counts.
            merge[key] = value

    keys, values = zip(*merge.items())
    values = [f'{-value}*' if value < 0 else str(value) for value in values]
    return keys, values
