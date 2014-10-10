#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 09/Oct/2014 6:48 PM

from schematics.models import Model
from schematics.types import StringType, IntType
from tornado.web import RequestHandler


class RequestModel(Model):
    def __init__(self, raw_data=None, deserialize_mapping=None, strict=True):
        data = {}
        if isinstance(raw_data, RequestHandler):
            for key in raw_data.request.arguments.keys():
                data[key] = raw_data.get_argument(key)
        elif isinstance(raw_data, dict):
            for key, value in raw_data.items():
                data[key] = value[0] if len(value) == 1 else value
        super(RequestModel, self)\
            .__init__(data or None, deserialize_mapping, strict)


class SignIn(RequestModel):
    footprint = StringType(required=True)
    device = StringType()
    device_os = StringType()
    device_carrier = StringType()
    device_lang = StringType()
    device_time_zone = IntType()
    device_mac_address = StringType()
    client_id = StringType(required=True)
    client_version = StringType(required=True)


class SignOut(SignIn):
    uid = StringType(required=True)