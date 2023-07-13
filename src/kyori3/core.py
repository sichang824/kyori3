#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kyori3.utils import check_callable
from kyori3.log import logger

__RPC_FUNCTIONS = {}

__all__ = ['export', 'call', 'inspect', 'RPCFunctions']


def export(*args, version='v2', **kwargs):
    """
    export function
    """

    def wrapper(func, mapping=None):

        if not mapping and args:
            mapping = args[0]
        if not mapping and 'mapping' in kwargs:
            mapping = kwargs['mapping']
        if not mapping:
            mapping = func.__name__

        item = {mapping: func}

        if not version in __RPC_FUNCTIONS:
            __RPC_FUNCTIONS.update({version: {}})

        if not mapping in __RPC_FUNCTIONS[version]:
            __RPC_FUNCTIONS[version].update(item)
            logger.debug(
                f"Export function: {func}, mapping: {mapping}, version: {version}"
            )
        return func

    # export(test1, test)
    if len(args) > 1:
        for func in args:
            wrapper(func, func.__name__)
    # export(test)
    elif len(args) == 1 and check_callable(args[0]):
        wrapper(args[0], args[0].__name__)
    # export({"test4": test})
    elif len(args) == 1 and isinstance(args[0], dict):
        for mapping, func in args[0].items():
            wrapper(func, mapping)
    # export(test5=test, test6=test)
    elif kwargs and 'mapping' not in kwargs:
        for mapping, func in kwargs.items():
            wrapper(func, mapping)
    # @export()
    # @export("test7")
    # @export(mapping="test8")
    else:
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


def call(fn, args=(), kwargs={}, version="v2"):
    try:
        func = __import(fn, version)
    except KeyError:
        func = None

    if not func: raise NameError(fn)

    try:
        return func(*args, **kwargs)
    except Exception as e:
        return e
