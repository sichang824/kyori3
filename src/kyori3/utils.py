#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast


def safe_eval(s):
    try:
        return ast.literal_eval(s)
    except ValueError:
        return s


def check_callable(value):

    try:
        # for instances of class or class
        return hasattr(value, '__dict__')
    except:
        pass

    try:
        # for Python 2.x or for Python 3.2+
        return callable(value)
    except:
        pass

    try:
        # for Python 3.x but before 3.2
        return hasattr(value, '__call__')
    except:
        pass