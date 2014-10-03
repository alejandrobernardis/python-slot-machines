#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 02/Oct/2014 2:46 PM

from backend.api.base import BaseHandler

handlers_list = [
    (r'/session/sign/in/?', None),
    (r'/session/sign/out/(?P<sid>\d+)/?', None)
]
