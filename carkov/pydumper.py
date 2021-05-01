#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

"""
Serialize chain as a python structure.
"""

from io import TextIOBase
from . import version
from .chain import Chain

template = """
# serialized from version {version}
def get_chainer():
    from carkov.chain import Chain
    from carkov.abstracts import NUMBER, TERMINAL, Abstract
    chain = Chain({order}, "{analyzer}")
    chain.data = {data}
    return chain
"""


def dump_chainer(chain: Chain, outfile: TextIOBase):
    """
    Serialize a chainer to an open IO stream

    Arguments:
        chain: A Chain object
        outfile: An open IO stream in text mode that will be writen to
    """
    outfile.write(template.format(version=version,
                                  order=chain.order,
                                  analyzer=chain.analyzer_class,
                                  data=repr(chain.data).replace(']},', ']},\n')))
