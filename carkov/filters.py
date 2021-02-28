#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

"""
Various filter functions that may be useful for processing certain kinds of corpora.
"""

from unidecode import unidecode


# All of these filters operate on string tokens

def str_abstractize_numbers(token):
    """Replace all numbers with a Number abstract."""
    pass

def str_abstractize_roman(token):
    """Replace roman numerals with a Number abstract."""
    pass

def str_strip_punct(token):
    """Remove any punctuation characters."""
    pass

def str_asciify(token):
    """Convert all characters to an ascii approximation."""
    pass
