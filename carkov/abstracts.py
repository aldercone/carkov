#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

"""
This module provides a few utility objects, especially the Abstract object which is used for terminals
and other abstract tokens.
"""

class CarkovFilterException(BaseException):
    pass

class Abort(CarkovFilterException):
    """
    This exception is intended for a protocol by which filters can abort a particular token from being added to the
    stream.
    """
    ...

class AbortSegment(CarkovFilterException):
    """
    This exception is intended for a protocol by which filters can abort an entire segment if a particular token would
    be rejected.
    """
    ...

class Abstract:
    """
    This is used as a way to indicate abstract tokens in a stream of tokens.
    """
    def __init__(self, name):
        self.name = name

    def __repl__(self):
        return f"<Abstract: {self.name}>"


"""A universal Number abstract."""
NUMBER = Abstract("NUMBER")

"""A Universal Terminal abostract."""
TERMINAL = Abstract("TERMINAL")
