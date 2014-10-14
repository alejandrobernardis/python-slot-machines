#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 12/Oct/2014 20:50

import datetime
from backend.models.base import DocumentModel
from schematics.types import StringType, IntType, FloatType, BooleanType, \
    DateTimeType


class SessionData(DocumentModel):
    sid = StringType(required=True)
    level = IntType(default=0)
    points = FloatType(default=0.0)
    balance = FloatType(default=0.0)
    awards = IntType(default=0)
    award_available = BooleanType(default=False)
    award_value = IntType(default=0)
    award_begin_time = DateTimeType(default=datetime.datetime.utcnow)
    award_finish_time = DateTimeType(default=None)


class AISessionData(SessionData):
    start = DateTimeType(default=datetime.datetime.utcnow)
    start_level = IntType(default=0)
    start_points = FloatType(default=0.0)
    start_balance = FloatType(default=0.0)
    start_awards = IntType(default=0)


class ProfileData(SessionData):
    uid = StringType(required=True)
    fbuid = StringType(required=True)
    token = StringType(required=True)
    token8 = StringType(required=True)
    rsa_public = StringType(required=True)
    rsa_private = StringType(required=True)
    last_login = DateTimeType(default=datetime.datetime.utcnow)


class DeviceData(SessionData):
    uid = StringType(required=True)
    footprint = StringType(required=True)
    device = StringType(default=None)
    device_os = StringType(default=None)
    device_carrier = StringType(default=None)
    device_lang = StringType(default=None)
    device_time_zone = IntType(default=0)
    device_mac_address = StringType(default=None)
    client_id = StringType(required=True)
    client_version = StringType(required=True)
