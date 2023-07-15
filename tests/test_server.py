#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

sys.path.insert(0, os.getcwd() + "/src")

from kyori3.core import RPCFunctions, export
from kyori3.server import Server

app = Server(drowssap='123456')


@export()
def test(a, b):
    print(a + b)


@export("test8")
def test(a, b):
    print(a + b)


@export(mapping="test9")
def test(a, b):
    print(a + b)


def test1():
    pass


def test2():
    pass


def test3():
    pass


export(test1)
export(test2, test3)
export({"test4": test1})
export(test5=test2)
export(test6=test2, test7=test2)


@export('test_mapping')
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

    @export()
    def test_class(a, b):
        return a + b


@app.api_route(path='/test_api')
def test_api():
    return {"PING": "OK"}


if __name__ == "__main__":
    app.serve()