#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 07/Oct/2014 7:23 PM

from backend.api.base import BaseHandler


class SignInHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.get_json_response_and_finish('~~GET~~')

    def post(self, *args, **kwargs):
        self.get_json_response_and_finish('~~POST~~')


class SignOutHandler(BaseHandler):
    def delete(self, *args, **kwargs):
        pass


handlers_list = [
    (r'/s/sign/in(?P<uid>\/[a-z0-9]+)?/?', SignInHandler),
    (r'/s/sign/out/(?P<sid>[a-z0-9]+)/?', SignOutHandler)
]
