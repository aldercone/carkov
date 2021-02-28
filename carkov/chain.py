#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

"""
This module defines a chainer class which can process a count dictionary from an analyzer
and provides convenience functions for walking the chain.
"""


from collections import UserDict, deque

from .abstracts import TERMINAL
from .utils import merge_stats, convert_counts, weighted_stat_choice


def from_analyzer(analyzer):
    """
    Static initializer: Return a chainer with parameters and contents based on an analyzer instance.
    """
    chainer = Chain(analyzer.order, analyzer.__class__.__name__)
    chainer.integrate(analyzer.chain_counts)
    return chainer


class Chain(UserDict):
    def __init__(self, order, analyzer_class=None):
        """
        Initialize Chain class

        Arguments:
            order: The window size of this chainer.
        """
        self.order = order
        self.data = {}
        self.start_token = (None, ) * self.order
        self.analyzer_class = analyzer_class

    def integrate(self, counts):
        """
        Accept a counts dictionary and merge it with local data and recalculate statistical relationships between
        outcomes. The counts must be from an analyzer of the same order.

        Arguments:
            counts: A counts dictionary as contained in the analyzer's chain_counts
        """
        for key, count in counts.items():
            stat = convert_counts(count)
            if key in self.data:
                merge_stats(self.data[key], stat)
            else:
                self.data[key] = stat
        self.update_stats()

    def merge(self, other):
        """
        Merge a separate chainer's data into this chainer. They must be of the same order.

        Arguments:
           other (Chain): Another chain of the same order.
        """
        for key, stat in other.items():
            if key in self.data:
                merge_stats(self.data[key], stat)
            else:
                self.data[key] = stat
        self.update_stats()

    def update_stats(self):
        """
        Update all of the statistical ratios in the chain.
        """
        for token in self.data:
            self.update_stat(token)

    def update_stat(self, parent_token):
        """
        Update one specific set of statistical ratios in the chain.

        Arguments:
            parent_token: A windowed token tuple which points at the part of the chain to update
        """
        stat = self.data[parent_token]
        total = sum([s[0] for s in stat.values()])
        for it in stat.values():
            it[1] = int((it[0] / total) * 100)

    def add(self, parent_token, token):
        """
        Add a new count to the chain.

        Arguments:
            parent_token: A windowed token tuple which points to the location to add the new token.
            token: The token to add.
        """
        if parent_token not in self.data:
            self.data[parent_token] = {}

        if token in self.data[parent_token]:
            self.data[parent_token][token][0] += 1
            self.update_stat(parent_token)
        else:
            self.data[parent_token][token] = [1, 100]

    def select(self, parent_token, random_generator, weighted=False):
        """
        Select a token from a given parent token.

        Arguments:
           parent_token: A windowed token tuple
           random_generator: A random.Random instance
           weighted (bool, default=False): Whether to do a weighted select or a random select.

        Returns:
           A token
        """
        if not parent_token in self.data:
            return None
        if weighted:
            return weighted_stat_choice(random_generator, self.data[parent_token])
        else:
            return random_generator.choice(list(self.data[parent_token].keys()))

    def walk(self, random_generator, weighted=False, maximum=1000):
        """
        Return a list of tokens by walking the chain.

        Arguments:
            random_generator: A random.Random instance
            weighted: Whether to do a weighted select at each step.
            maximum: THe maximum number of walks to perform.

        Returns:
            A list of tokens
        """
        token = self.start_token
        item = None
        output = []
        while (len(output) < maximum):
            item = self.select(token, random_generator, weighted)
            if item == TERMINAL:
                return output
            output.append(item)
            token = self.next_token(token, item)

    def next_token(self, parent_token, token):
        """
        Given a windowed token tuple and a token, return the next windowed token tuple.

        Arguments:
            parent_token: A windowed token tuple
            token: A token

        Returns:
            A windowed token tuple which would be the next step in the chain after the token.
        """
        q = deque(parent_token, self.order)
        q.append(token)
        return tuple(q)
