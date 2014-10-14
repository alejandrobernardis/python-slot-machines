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


class ServiceHandler(BaseHandler):
    def _get_url(self, with_domain=True):
        url = '/s' + self.request.uri
        if with_domain:
            url = self.api_domain('http') + url
        return url

    @gen.coroutine
    def _set_request(self):
        response = None
        try:
            request = HTTPRequest(self._get_url())
            request.method = self.request.method
            request.headers = self.request.headers
            if self.request.method in ("POST", "DELETE", "PATCH", "PUT"):
                request.body = self.request.body
            response = yield AsyncHTTPClient().fetch(request)
            self.write(response.body)
        except Exception, e:
            self.get_json_exception_response_and_finish(e)
        raise gen.Return(response)

    def prepare(self):
        self.set_header_for_json()

    def compute_etag(self):
        return None

    @gen.coroutine
    def head(self, *args, **kwargs):
        yield self._set_request()

    @gen.coroutine
    def get(self, *args, **kwargs):
        yield self._set_request()

    @gen.coroutine
    def post(self, *args, **kwargs):
        yield self._set_request()

    @gen.coroutine
    def delete(self, *args, **kwargs):
        yield self._set_request()

    @gen.coroutine
    def patch(self, *args, **kwargs):
        yield self._set_request()

    @gen.coroutine
    def put(self, *args, **kwargs):
        yield self._set_request()

    @gen.coroutine
    def options(self, *args, **kwargs):
        yield self._set_request()


handlers_list = [
    (r'/sign/in(?P<uid>\/[a-z0-9]+)?/?', ServiceHandler),
    (r'/sign/out/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/game/find_golden_eggs/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/game/roulette/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/game/slot/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/store/android/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/store/ios/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/media/nags/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/social/sync/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/social/gift/request/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/social/gift/send/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/social/invite/send/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/social/notifications/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/social/share/bonus/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/session/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/session/balance/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/session/bonus/(?P<sid>[a-z0-9]+)/?', ServiceHandler),
    (r'/session/slots/(?P<sid>[a-z0-9]+)/?', ServiceHandler)
]
