#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 14/Oct/2014 14:36

from backend.models.db.profiles import SessionData
from schematics.types import IntType, FloatType, BooleanType


class SlotModel(SessionData):
    bet = FloatType(default=0)
    lines = IntType(default=0)
    games = IntType(default=0)
    game_available = BooleanType(default=False)
    game_value = IntType(default=0)
    free_spins = IntType(default=0)
    free_spins_available = BooleanType(default=False)
    free_spins_value = IntType(default=0)