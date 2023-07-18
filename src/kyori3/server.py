#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import ssl
from http import HTTPStatus
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

from kyori3.log import logger, LogRawStrings as lrs
from kyori3.utils import safe_eval
from kyori3.core import call, inspect

from kyori3.constant import (
    RPC_CONTENT_TYPE_HEADER,
    RPC_SSL,
    RPC_SSL_KEY_FILE,
    RPC_SSL_CERT_FILE,
    RPC_URL_ENDPOINT,
)

__all__ = ['Server']


class ServerHandler(BaseHTTPRequestHandler):

    def __set_content_type(self, _type):
        _type_str = RPC_CONTENT_TYPE_HEADER + _type.__name__
        logger.debug(lrs.type_setting, _type_str)
        self.send_header('Content-type', _type_str)

    def __set_headers(self, _type=str, **kwargs):
        if not 'content_type' in kwargs:
            self.__set_content_type(_type)
        for kwarg, value in kwargs.items():
            kwarg = kwarg.replace('_', '-')
            kwarg = kwarg.capitalize()
            self.send_header(kwarg, value)
        self.end_headers()

    def __get_payload(self):
        length = self.headers.get("Content-Length", 0)
        if length: nbytes = int(length)
        return self.rfile.read(nbytes).decode()

    def __parse_payload(self):
        func, args, kwargs = safe_eval(self.__get_payload())
        return func, args, kwargs

    def __get_rpc_version(self):
        return self.headers.get("RPC-version", '')

    def do_HEAD(self):
        fn = self.__get_payload()
        logger.info(lrs.heading, fn)
        if inspect(fn, self.__get_rpc_version()):
            self.send_response(HTTPStatus.OK)
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
        self.__set_headers()

    def do_POST(self):
        """
        Get function to execute
        """
        if self.path in RPC_URL_ENDPOINT:
            try:
                func, args, kwargs = self.__parse_payload()
            except Exception:
                self.send_response(HTTPStatus.BAD_REQUEST, lrs.no_payload)
                self.__set_headers()
            else:
                logger.info(lrs.execute, func, args, kwargs)
                result = call(func, args, kwargs, self.__get_rpc_version())
                logger.debug(lrs.result, result)
                self.send_response(HTTPStatus.OK, result)
                self.__set_headers(type(result))
        else:
            if not self.path in self.server.ROUTES:
                self.send_response(HTTPStatus.NOT_FOUND)
            else:
                data = json.dumps(self.server.ROUTES[self.path]())
                self.send_response(HTTPStatus.OK, data)
            self.__set_headers(content_type='application/json; charset=utf-8')


class Server(object):

    ROUTES = {}

    def __init__(
        self,
        addr=None,
        handler=None,
        securely=False,
        key_file=None,
        cert_file=None,
        drowssap=None,
    ):
        self.addr = addr or ("0.0.0.0", 8000)
        self.handler = handler or ServerHandler

        self.securely = securely or RPC_SSL
        self.key_file = key_file or RPC_SSL_KEY_FILE
        self.cert_file = cert_file or RPC_SSL_CERT_FILE
        self.ssap = drowssap

    def api_route(self, path):
        """
        route function
        """

        def wrapper(func):

            self.ROUTES.update({path: func})

            def inner(*args, **kwargs):
                return func(*args, **kwargs)

            return inner

        return wrapper

    def serve(self):
        server = ThreadingHTTPServer(self.addr, self.handler)
        server.ROUTES = self.ROUTES

        if all([self.securely, self.key_file, self.cert_file]):
            logger.debug(lrs.load_ssl, self.key_file, self.cert_file)
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            if self.ssap:
                ctx.load_cert_chain(self.cert_file, self.key_file, self.ssap)
            else:
                ctx.load_cert_chain(self.cert_file, self.key_file)

            server.socket = ctx.wrap_socket(server.socket, server_side=True)

        logger.info(lrs.server_starting, self.addr)
        server.serve_forever()
        logger.info(lrs.server_shutdown)
