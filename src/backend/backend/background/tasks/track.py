#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 14/Oct/2014 18:31

from backend.background.server import celery, celery_logging


@celery.task(ignore_result=True)
def push__track_activity(*args, **kwargs):
    try:
        return True
    except Exception, e:
        return celery_logging(e)
