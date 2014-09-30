#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 01/Oct/2013 10:05

from  slots.common.utils import random_and_probability
from  slots.handlers.base import BaseHandler
from  slots.security.sessions import session_verify


S3_URL = 'http://cdn.domain.tld/static/nags/{}'
NAGS_SCREEN_PROBABILITY = (.4, .4, .3, .09, .3,)
NAGS_SCREEN_TOLERANCE = .000001
NAGS_SCREEN_TOTAL = 2

NAGS_SCREEN = (
    dict(
        nid=4,
        image=S3_URL + '/nag_0004.jpg',
        url=None,
        action='buy_conis',
    ),
    dict(
        nid=5,
        image=S3_URL + '/nag_0005.jpg',
        url=None,
        action='social_send',
    ),
    dict(
        nid=1,
        image=S3_URL + '/nag_0001.jpg',
        url=None,
        action='buy_conis',
    ),
    dict(
        nid=3,
        image=S3_URL + '/nag_0003.jpg',
        url=None,
        action='social_invite',
    ),
    dict(
        nid=2,
        image=S3_URL + '/nag_0002.jpg',
        url=None,
        action='social_request',
    ),
)


class NagsListHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        session = self.session.data
        device = session.get('device', 'ipad')
        result = []
        while len(result) < NAGS_SCREEN_TOTAL:
            value = random_and_probability(
                NAGS_SCREEN_PROBABILITY, NAGS_SCREEN_TOLERANCE)
            nag = NAGS_SCREEN[value].copy()
            nag['image'] = nag['image'].format(device.lower())
            if nag not in result:
                result.append(nag)
        self.get_json_response_and_finish(response=result)


handlers_list = [
    (r'/do/nags/list', NagsListHandler)
]
