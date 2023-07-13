#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

sys.path.insert(0, os.getcwd() + "/src")

import ssl
import unittest
from kyori3.client import HTTPClient, HTTPSClient
from kyori3.constant import RPC_SSL, RPC_SSL_KEY_FILE, RPC_SSL_CERT_FILE

if RPC_SSL:
    # ssap: 123456
    client = HTTPSClient(
        "localhost",
        8000,
        key_file=RPC_SSL_KEY_FILE,
        cert_file=RPC_SSL_CERT_FILE,
        context=ssl._create_unverified_context(),
    )
else:
    client = HTTPClient("localhost", 8000)


class Test(unittest.TestCase):

    def test_mapping(self):
        assert client.test_mapping(1, 2) == 3

    def test_add(self):
        assert client.test_add(1, 2) == 3

    def _test_type(self, data, _type):
        func = getattr(client, f'test_{_type.__name__}')
        result = func(data)
        assert result == data
        assert type(result) == _type

    def test_str(self):
        self._test_type("OK", str)

    def test_int(self):
        self._test_type(0, int)
        self._test_type(1, int)
        self._test_type(5, int)

    def test_dict(self):
        self._test_type({"A": "a"}, dict)

    def test_list(self):
        self._test_type(['A', 'a'], list)

    def test_tuple(self):
        self._test_type(('A', 'a'), tuple)

    def test_float(self):
        self._test_type(5.555, float)

    def test_bool(self):
        self._test_type(True, bool)
        self._test_type(False, bool)

    def test_function(self):
        try:
            client.test_dict(client)
        except Exception as e:
            assert isinstance(e, TypeError)

        try:
            client.test_dict(client=client)
        except Exception as e:
            assert isinstance(e, TypeError)

    def test_params(self):
        assert client.test_params(1, 2, c=4, d=5, e=6) == (1, 2, 4, (), {
            'd': 5,
            'e': 6
        })
        assert client.test_params(1, 2, 3, 4, d=5) == (1, 2, 3, (4, ), {
            'd': 5
        })

    def test_not_found(self):
        try:
            client.test_not_found()
        except Exception as e:
            assert isinstance(e, ModuleNotFoundError)

    def test_local_func(self):
        assert client.test_func("test") == "test"
        assert client.test_func(1) == 1

    def test_add_rcall(self):
        assert client.rcall("test_add", 1, 2) == 3
        assert client.rcall("test_add", 2, 2) == 4

    def test_class(self):
        assert client.rcall("test_class", 1, 2) == 3


def main():
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main(argv=['ignored', '-v'], exit=False)
    # unittest.main(argv=['ignored', '-v',"Test.test_class"], exit=False)


if __name__ == "__main__":
    main()
