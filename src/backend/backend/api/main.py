#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 23/Sep/2014 7:33 AM

from backend.api.base import BaseHandler


class MainHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.get_json_response_and_finish({
            'name': self.settings.get('app_name'),
            'version': self.settings.get('app_version')
        })


handlers_list = [
    (r'/', MainHandler)
]
