#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 09/Oct/2014 6:48 PM

from backend.models.base import RequestModel
from schematics.types import StringType, IntType


class SignInRequest(RequestModel):
    footprint = StringType(required=True)
    device = StringType()
    device_os = StringType()
    device_carrier = StringType()
    device_lang = StringType()
    device_time_zone = IntType()
    device_mac_address = StringType()
    client_id = StringType(required=True)
    client_version = StringType(required=True)


class SignOutRequest(SignInRequest):
    uid = StringType(required=True)
