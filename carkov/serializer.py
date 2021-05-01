#
# carkov markov chain library
# © Copyright 2021 by Aldercone Studio <aldercone@gmail.com>
# This is free software, see the included LICENSE for terms and conditions.
#

"""
Use msgpack to serialize a chainer to disk and then reread it from a serialized file.
"""

from typing import Any, BinaryIO, Dict, Tuple, cast

import msgpack

from . import version
from .abstracts import NUMBER, TERMINAL, Abstract
from .chain import Chain


def _unserialize_encode_helper(obj: Dict) -> Any:
    """
    This is a helper function which handles Abstract objects for serialization.
    """
    if '$$####$$' in obj:
        val: Abstract
        if obj['n'] == 'TERMINAL':
            val = TERMINAL
        elif obj['n'] == 'NUMBER':
            val = NUMBER
        else:
            val = Abstract(obj['n'])
        return val
    return obj


def _serialize_encode_helper(obj: Any) -> Any:
    """
    This is a helper function which handles Abstract objects for serialization.
    """
    if isinstance(obj, Abstract):
        obj = {'$$####$$': True, 'n': cast(Abstract, obj).name}
    return obj


def load_chainer(infile: BinaryIO) -> Chain:
    """
    Unserialize a chainer from an open IO stream

    Arguments:
        infile: An open IO stream in binary mode pointing at a messagepack stream

    Returns:
        a new Chain object initialized with the contents of the stream.
    """
    serialdict = msgpack.unpackb(infile.read(), object_hook=_unserialize_encode_helper, raw=False)
    if serialdict['version'] != version:
        import warnings
        warnings.warn(f"Version mismatch while loading chain expect: [{version}] got: [{serialdict['version']}]")
    chain = Chain(serialdict['order'], serialdict['analyzer_class'])
    chain.data = {cast(Tuple[Any], tuple(x)): y for x, y in serialdict['data']}
    return chain


def dump_chainer(chain: Chain, outfile: BinaryIO):
    """
    Serialize a chainer to an open IO stream

    Arguments:
        chain: A Chain object
        outfile: An open IO stream in binary mode that will be writen to
    """
    serialdict: Dict[str, Any] = {}
    serialdict['version'] = version
    serialdict['order'] = chain.order
    serialdict['analyzer_class'] = chain.analyzer_class
    serialdict['data'] = [(k, v) for k, v in chain.items()]
    outfile.write(msgpack.packb(serialdict, use_bin_type=True, default=_serialize_encode_helper))
