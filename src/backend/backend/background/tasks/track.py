#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 14/Oct/2014 18:31

from backend.background.server import celery, celery_logging, celery_collection
from backend.models.base import get_logic_low
from tornado import gen


@gen.coroutine
def track_activity(collection, activity, message, **kwargs):
    try:
        query = get_logic_low(kwargs)
        query['activity'] = activity
        query['message'] = message
        response = yield celery_collection(collection, 'tracker')\
            .insert(query, w=0, j=False)
        raise gen.Return(response)
    except Exception, e:
        celery_logging(e)


@celery.task()
def push__track_activity(collection, activity, message, **kwargs):
    try:
        yield track_activity(collection, activity, message, **kwargs)
    except Exception, e:
        celery_logging(e)
