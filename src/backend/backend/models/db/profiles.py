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
    sid_parent = StringType(required=True)
    puid = StringType()
    duid = StringType(required=True)
    level = IntType(default=0)
    points = FloatType(default=0.0)
    balance = FloatType(default=0.0)
    start_level = IntType(default=0)
    start_points = FloatType(default=0.0)
    start_balance = FloatType(default=0.0)
    start_awards = IntType(default=0)
    awards = IntType(default=0)
    award_available = BooleanType(default=False)
    award_value = IntType(default=0)
    award_begin_time = DateTimeType(default=datetime.datetime.utcnow)
    award_finish_time = DateTimeType(default='')
    award_finish_time_value = IntType(default=0)



class ProfileData(DocumentModel):
    puid = StringType(required=True)
    fbuid = StringType(required=True)
    token = StringType(required=True, max_length=64)
    token8 = StringType(required=True, min_length=8, max_length=8)
    rsa_public = StringType(required=True)
    rsa_private = StringType(required=True)
    last_sid = StringType()


class DeviceData(DocumentModel):
    duid = StringType(required=True)
    footprint = StringType(required=True)
    device = StringType(default='')
    device_os = StringType(default='')
    device_carrier = StringType(default='')
    device_lang = StringType(default='')
    device_time_zone = IntType(default=0)
    device_mac_address = StringType(default='')
    ios_advertising_id = StringType(default='')
    ios_gamecenter_id = StringType(default='')
    client_id = StringType(required=True)
    client_version = StringType(required=True)
    last_sid = StringType()