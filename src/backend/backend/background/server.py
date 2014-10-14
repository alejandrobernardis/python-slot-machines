#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 23/Sep/2014 6:02 AM

from __future__ import absolute_import

__all__ = (
    'celery',
    'celery_database',
    'celery_collection',
    'celery_logger',
    'celery_logging'
)


import global_settings
from backend.common.storage import nosql_database_connector
from celery import Celery
from celery.utils.log import get_task_logger


celery = Celery()
celery.config_from_object('backend.background.settings')
celery_logger = get_task_logger(__name__)

_db_cache = {}


def celery_database(name):
    global _db_cache
    if name not in _db_cache:
        _db_cache[name] = \
            nosql_database_connector(name, global_settings.DATABASE)
    return _db_cache[name]


def celery_collection(name, database='default'):
    return celery_database(database)[name]


def celery_logging(exception, level='error', *args, **kwargs):
    try:
        message = getattr(exception, 'message', False) or str(exception)
        celery_logger[level](message, *args, **kwargs)
    except Exception, e:
        celery_logger.critical(e, *args, **kwargs)
    return True


if __name__ == '__main__':
    celery.start()