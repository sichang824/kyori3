#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Client Settings
RPC_RELEASE_VERSION = "v2"
RPC_DEFAULT_HEADERS = {'RPC-version': RPC_RELEASE_VERSION}
RPC_URL_ENDPOINT = "/"
RPC_HEAD_FUNCTION_METHOD = "HEAD"
RPC_CALL_FUNCTION_METHOD = "POST"

# Content-type
RPC_FUNCTION_TYPE = "raw/function"
RPC_CONTENT_TYPE_FMT = ("raw", "/", "")
RPC_CONTENT_TYPE_HEADER = "".join(RPC_CONTENT_TYPE_FMT)

# SSL
RPC_SSL = False
RPC_SSL_KEY_FILE = "/Users/sichang/projects/octopus/rpc/key.pem"
RPC_SSL_CERT_FILE = "/Users/sichang/projects/octopus/rpc/cert.pem"
