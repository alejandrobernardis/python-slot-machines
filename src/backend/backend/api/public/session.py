#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 02/Oct/2014 2:46 PM

from backend.api.base import BaseHandler
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class RouterHandler(BaseHandler):
    def _get_api_url(self, with_domain=True):
        url = '/s' + self.request.uri
        if with_domain:
            url = self.api_domain('http') + url
        return url

    def _get_async_client(self):
        request = HTTPRequest(self._get_api_url())
        request.method = self.request.method
        request.headers = self.request.headers
        if self.request.method in ("POST", "DELETE", "PATCH", "PUT"):
            request.body = self.request.body
        return AsyncHTTPClient().fetch(request)

    def prepare(self):
        self.trace_request()
        self.set_header_for_json()

    @gen.coroutine
    def get(self, *args, **kwargs):
        response = yield self._get_async_client()
        self.finish(response.body)

    @gen.coroutine
    def post(self, *args, **kwargs):
        response = yield self._get_async_client()
        self.finish(response.body)


handlers_list = [
    (r'/sign/in(?P<uid>\/[a-z0-9]+)?/?', RouterHandler),
    (r'/sign/out/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/game/find_golden_eggs/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/game/roulette/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/game/slot/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/store/android/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/store/ios/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/pop/nags/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/social/sync/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/social/gift/request/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/social/gift/send/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/social/invite/send/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/social/notifications/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/social/share/bonus/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/session/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/session/balance/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/session/bonus/(?P<sid>[a-z0-9]+)/?', RouterHandler),
    (r'/session/slots/(?P<sid>[a-z0-9]+)/?', RouterHandler),
]
