import random
import re
import string
import unicodedata
from collections import OrderedDict
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest
from typing import List, Optional, Tuple, Iterator

import unidecode


def char_filter(s: str) -> Iterator[str]:
    """Returns a generator of characters that are properly converted from their unicode character into their ASCII equivalent."""
    latin = re.compile('[a-zA-Z]+')
    for char in unicodedata.normalize('NFC', s):
        decoded = unidecode.unidecode(char)
        if latin.match(decoded):
            yield char
        else:
            yield decoded


def clean_string(s: str) -> str:
    """Returns a clean string, devoid of ugly Unicode characters."""
    return "".join(char_filter(s))


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
