#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 13/Oct/2014 3:11

import re
import copy
import datetime
from schematics.models import Model
from schematics.types import BooleanType, DateTimeType
from tornado.web import RequestHandler
from unicodedata import normalize, category

__all__ = (
    'get_logic_low',
    'remove_accents',
    'add_accents',
    'DocumentModel'
)


ACCENTS = (
    ('a', u'aàáâãäå'),
    ('e', u'eèéêë'),
    ('i', u'iìíîï'),
    ('o', u'oòóôõö'),
    ('u', u'uùúûü'),
    ('c', u'cç'),
    ('n', u'nñ'),
    ('y', u'yýÿ')
)


def get_logic_low(query, enabled=True, available=True, date=None):
    if not isinstance(query, dict):
        return query
    if not isinstance(date, (datetime.date, datetime.datetime)):
        date = datetime.datetime.utcnow()
    data = {
        'available': available,
        'enabled': enabled,
        'created': date,
        'modified': date
    }
    data.update(copy.deepcopy(query))
    return data


def remove_accents(value):
    if not isinstance(value, unicode):
        value = unicode(value)
    return ''.join(c for c in normalize('NFD', value) if category(c) != 'Mn')


def add_accents(value, regex=False):
    if not isinstance(value, (basestring, unicode)):
        raise TypeError('Invalid type, must be a basestring or unicode.')
    value = remove_accents(value)
    for k, v in ACCENTS:
        value = value.replace(k, '[%s]' % v)
    return value if not regex else re.compile(value, re.I)


class RequestModel(Model):
    _errors = None

    def __init__(self, raw_data=None, deserialize_mapping=None, strict=True):
        data = {}
        if isinstance(raw_data, RequestHandler):
            for key in raw_data.request.arguments.keys():
                data[key] = raw_data.get_argument(key)
        super(RequestModel, self)\
            .__init__(data or None, deserialize_mapping, strict)

    def validate(self, partial=False, strict=False):
        try:
            super(RequestModel, self).validate(partial, strict)
            return True
        except Exception, e:
            self._errors = getattr(e, 'messages')
            return False

    @property
    def errors(self):
        return self._errors


class DocumentModel(Model):
    created = DateTimeType(default=datetime.datetime.utcnow)
    modified = DateTimeType(default=datetime.datetime.utcnow)
    enabled = BooleanType(default=True)
    available = BooleanType(default=True)
