#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from core import RPCFunctions, export
from server import Server

from log import logger

app = Server(drowssap='123456')


@export(mapping='test_mapping')
def test_add(a, b):
    return a + b


@export()
def test_add(a, b):
    return a + b


@export()
def test_str(d):
    assert type(d) == str
    return d


@export()
def test_int(d):
    assert type(d) == int
    return d


@export()
def test_dict(d):
    assert type(d) == dict
    return d


@export()
def test_list(d):
    assert type(d) == list
    return d


@export()
def test_tuple(d):
    assert type(d) == tuple
    return d


@export()
def test_float(d):
    assert type(d) == float
    return d


@export()
def test_bool(d):
    assert type(d) == bool
    return d


@export()
def test_params(a, b, c, *args, **kwargs):
    return a, b, c, args, kwargs


class TestInclude(RPCFunctions):

    def test_add(a, b):
        return a + b

    def test_add(a, b):
        return a + b

    def test_str(d):
        assert type(d) == str
        return d

    def test_int(d):
        assert type(d) == int
        return d

    def test_dict(d):
        assert type(d) == dict
        return d

    def test_list(d):
        assert type(d) == list
        return d

    def test_tuple(d):
        assert type(d) == tuple
        return d

    def test_float(d):
        assert type(d) == float
        return d

    def test_bool(d):
        assert type(d) == bool
        return d

    def test_params(a, b, c, *args, **kwargs):
        return a, b, c, args, kwargs


if __name__ == "__main__":
    app.serve()