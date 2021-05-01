#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

from .abstract import AbstractAnalyzer


class Words(AbstractAnalyzer):
    def __init__(self, order, filters=None):
        if filters is None:
            filters = []
        super().__init__(order, filters)

    def segmentize_corpus(self, corpus):
        return corpus.split(' ')

    def tokenize_segment(self, segment):
        return list(segment)
