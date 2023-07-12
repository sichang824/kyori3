#!/usr/bin/env python
# -*- coding: utf-8 -*-

from log import logger

__RPC_FUNCTIONS = {}

__all__ = ['export', 'call', 'inspect', 'RPCFunctions']


def export(mapping=None, version='v2'):
    """
    export function
    """

    def wrapper(func):
        fn = mapping or func.__name__
        item = {fn: func}

        if not version in __RPC_FUNCTIONS:
            __RPC_FUNCTIONS.update({version: {}})
        __RPC_FUNCTIONS[version].update(item)
        logger.debug(
            f"Export function: {func}, mapping: {mapping}, version: {version}")

        return func

    return wrapper


class RPCFunctions(object):
    """
    export all functions in the class
    """


def inspect(fn, version):
    return __import(fn, version) is not None


def __import(fn, version):
    """
    import from mem
    """
    return __RPC_FUNCTIONS[version].get(fn, None)


def call(fn, args, kwargs, version):
    func = __import(fn, version)
    if not func: raise NameError(fn)
    return func(*args, **kwargs)
