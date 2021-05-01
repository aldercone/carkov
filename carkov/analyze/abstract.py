#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

from abc import ABC, abstractmethod
from collections import deque, defaultdict

from ..abstracts import TERMINAL
from ..utils import merge_dict

"""
This module defines the base class for analyzers which do basic statistical analysis on a corpus.
"""


class AbstractAnalyzer(ABC):
    def __init__(self, order, filters=None):
        """
        Initialize the analyzer.

        Arguments:
          order (int): Defines the window size this analyzer uses.
          filters: A list of callables to apply to each token before processing.
        """
        if filters is None:
            filters = []
        self.order = order
        self.filters = filters
        self.tokens = {}
        self.chain_counts = {}

    def analyze(self, corpus):
        """
        Analyze a corpus and integrate the data into the internal state.

        Arguments:
           corpus (abstract): This could be any type that the class is prepared to process.

        Retruns:
           self.chain_counts after processing.
        """
        counts = self.analyze_corpus(corpus)
        merge_dict(self.chain_counts, counts)
        return self.chain_counts

    def analyze_corpus(self, corpus):
        """
        Do the actual analysis of corpus, and return a count dictionary.

        Arguments:
           corpus (abstract): This could be any type that the class is prepared to process.

        Returns:
           (dict) a count dictionary of just this corpus
        """
        segments = self.segmentize_corpus(corpus)
        counts = {}
        for segment in segments:
            merge_dict(counts, self.analyze_segment(segment))

        return counts

    @abstractmethod
    def segmentize_corpus(self, corpus):
        """
        Convert a corpus into a series of segments.

        This must be overloaded by child class.

        Arguments:
           corpus (abstract): This could be any type that the class is prepared to process.

        Returns:
           (array of abstract): An array of segments that this class is prepared to process.
        """

    def analyze_segment(self, segment):
        """
        Process a segment into a series of tokens.

        Arguments:
           segment (abstract): This could be of any type that this class is prepared to process.

        Returns:
           (counts dictionary): A dictionary keyed by windowed token keys with counts of each following token
        """
        tokens = self.tokenize_segment(segment) + [TERMINAL]
        token = deque([None] * self.order, self.order)
        counts = defaultdict(lambda: defaultdict(int))
        for raw_token in tokens:
            raw_token = self.process_token(raw_token)
            tkey = tuple(token)
            counts[tkey][raw_token] += 1

            token.append(raw_token)
        return counts

    @abstractmethod
    def tokenize_segment(self, segment):
        """
        Convert a segment into a series of tokens.

        This must be overloaded by child class.

        Arguments:
           segment (abstract): This could be of any type that this class is prepared to process.

        Returns:
           (array of tokens): The format and type of tokens is defined by the child class.

        """

        ...

    def process_token(self, raw_token):
        for filter in self.filters:
            raw_token = filter(raw_token)
        return raw_token
