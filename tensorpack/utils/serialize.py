#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: serialize.py


import msgpack
import msgpack_numpy
msgpack_numpy.patch()

try:
    # https://github.com/apache/arrow/pull/1223#issuecomment-359895666
    import sys
    old_mod = sys.modules.get('torch', None)
    sys.modules['torch'] = None
    import pyarrow as pa
    if old_mod is not None:
        sys.modules['torch'] = old_mod
    else:
        del sys.modules['torch']
except ImportError:
    pa = None


__all__ = ['loads', 'dumps']


def dumps_msgpack(obj):
    """
    Serialize an object.
    Returns:
        Implementation-dependent bytes-like object
    """
    return msgpack.dumps(obj, use_bin_type=True)


def loads_msgpack(buf):
    """
    Args:
        buf: the output of `dumps`.
    """
    return msgpack.loads(buf, raw=False)


def dumps_pyarrow(obj):
    """
    Serialize an object.

    Returns:
        Implementation-dependent bytes-like object
    """
    return pa.serialize(obj).to_buffer()


def loads_pyarrow(buf):
    """
    Args:
        buf: the output of `dumps`.
    """
    return pa.deserialize(buf)


if pa is None:
    loads = loads_msgpack
    dumps = dumps_msgpack
else:
    loads = loads_pyarrow
    dumps = dumps_pyarrow
