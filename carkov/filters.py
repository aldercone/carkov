#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

"""
Various filter functions that may be useful for processing certain kinds of corpora.
"""

from typing import Optional

# from unidecode import unidecode # fixme asciifying filter


# All of these filters operate on string tokens

def str_abstractize_numbers(token: str) -> Optional[str]:
    """Replace all numbers with a Number abstract."""
    return None


def str_abstractize_roman(token: str) -> Optional[str]:
    """Replace roman numerals with a Number abstract."""
    return None


def str_strip_punct(token: str) -> Optional[str]:
    """Remove any punctuation characters."""
    return None


def str_asciify(token: str) -> Optional[str]:
    """Convert all characters to an ascii approximation."""
    return None
