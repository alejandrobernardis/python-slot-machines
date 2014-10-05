#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 02/Oct/2014 2:46 PM

from backend.api.base import BaseHandler


class SignInHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


class SignOutHandler(BaseHandler):
    def delete(self, *args, **kwargs):
        pass


handlers_list = [
    (r'/sign/in/(?P<uid>\d+)?/?', None),
    (r'/sign/out/(?P<sid>\d+)/?', None),
    (r'/game/find_golden_eggs/(?P<sid>\d+)/?', None),
    (r'/game/roulette/(?P<sid>\d+)/?', None),
    (r'/game/slot/(?P<sid>\d+)/?', None),
    (r'/store/android/(?P<sid>\d+)/?', None),
    (r'/store/ios/(?P<sid>\d+)/?', None),
    (r'/pop/nags/(?P<sid>\d+)/?', None),
    (r'/social/sync/(?P<sid>\d+)/?', None),
    (r'/social/gift/request/(?P<sid>\d+)/?', None),
    (r'/social/gift/send/(?P<sid>\d+)/?', None),
    (r'/social/invite/send/(?P<sid>\d+)/?', None),
    (r'/social/notifications/(?P<sid>\d+)/?', None),
    (r'/social/share/bonus/(?P<sid>\d+)/?', None),
    (r'/session/(?P<sid>\d+)/?', None),
    (r'/session/balance/(?P<sid>\d+)/?', None),
    (r'/session/bonus/(?P<sid>\d+)/?', None),
    (r'/session/slots/(?P<sid>\d+)/?', None),
]
