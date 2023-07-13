#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydoc import locate
from http import HTTPStatus
from http.client import HTTPSConnection, HTTPConnection

from kyori3.log import logger
from kyori3.utils import safe_eval, check_callable

from kyori3.constant import (
    RPC_DEFAULT_HEADERS,
    RPC_URL_ENDPOINT,
    RPC_FUNCTION_TYPE,
    RPC_HEAD_FUNCTION_METHOD,
    RPC_CALL_FUNCTION_METHOD,
    RPC_CONTENT_TYPE_HEADER,
)

__all__ = ['HTTPClient', 'HTTPSClient']


class BaseClient(object):

    FN_CACHE = ""

    def __req(self, method, payload, headers):

        try:
            self.request(method, RPC_URL_ENDPOINT, payload, headers)
            resp = self.getresponse()

        except ConnectionRefusedError:
            msg = "Failed to connect to the server, maybe the server is not ready."
            logger.error(msg)
            raise ConnectionResetError(msg)
        except ConnectionResetError:
            msg = "Failed to connect to the server, try ssl connection."
            logger.error(msg)
            raise ConnectionResetError(msg)

        resp.close()
        return resp

    def __gen_headers(self, **kwargs):
        kwargs.update(RPC_DEFAULT_HEADERS)
        return kwargs or RPC_DEFAULT_HEADERS

    def __head_function(self, fn):
        headers = self.__gen_headers(Content_type=RPC_FUNCTION_TYPE)
        resp = self.__req(RPC_HEAD_FUNCTION_METHOD, fn, headers)
        return resp.status == HTTPStatus.OK

    def __gen_payload(self, fn, args, kwargs):

        for arg in list(args) + list(kwargs.values()):
            if check_callable(arg):
                raise TypeError(f"Function not allowed in args: {arg}")

        return str((fn, args, kwargs)).encode()

    def __parse_resp(self, resp):
        content_type = resp.getheader("Content-type", None)
        _type = locate(content_type.lstrip("raw/"))

        if issubclass(_type, Exception):
            raise _type(resp.reason)

        if content_type and content_type.startswith(RPC_CONTENT_TYPE_HEADER):
            return safe_eval(resp.reason)
        else:
            return resp.reason

    def function(self, *args, **kwargs):
        fn = self.FN_CACHE
        self.FN_CACHE = ""
        payload = self.__gen_payload(fn, args, kwargs)
        resp = self.__req(
            RPC_CALL_FUNCTION_METHOD,
            payload,
            self.__gen_headers(),
        )
        return self.__parse_resp(resp)

    def __getattr__(self, fn):
        """ 
        优先尝试在本地获取函数，如果没找到，head rpc server端查找
        用HEAD方法直接访问服务端，如果服务端存在对应的函数，响应的状态是200
        """
        if fn in self.__dict__:
            return getattr(self, fn)

        if not self.__head_function(fn):
            raise ModuleNotFoundError(
                f"No module found on the rpc server: {fn}")
        self.FN_CACHE = fn
        return self.function

    def rcall(self, fn, *args, **kwargs):
        """
        远程调用函数，包括位置传参和关键字传参，参数类型可以是Python任意的原生类型
        返回得到一个远程函数执行完毕以后返回值
        """
        if not self.__head_function(fn):
            raise ModuleNotFoundError(
                f"No module found on the rpc server: {fn}")
        self.FN_CACHE = fn
        return self.function(*args, *kwargs)

    def test_func(self, string):
        return string


class HTTPClient(HTTPConnection, BaseClient):
    pass


class HTTPSClient(HTTPSConnection, BaseClient):
    pass
