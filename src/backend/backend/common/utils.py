#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 23/Sep/2014 6:04 AM

import os
import copy
import datetime
import dateutil.parser
import json
import logging
import traceback
from backend.common.errors import ConfigurationError
from backend.common.regex import rx_isoformat, rx_isoformat_date, \
    rx_isoformat_time, rx_camel_case_split
from importlib import import_module
from itertools import izip


def swallow_args(func):
    def decorator(value, *args, **kwargs):
        if not value:
            return None
        return func(value, *args, **kwargs)
    return decorator


def is_primitive(value):
    return isinstance(value, (
        complex, int, float, long, bool, str, basestring, unicode, tuple, list))

@swallow_args
def domain(name, port=None, protocol=None):
    if isinstance(protocol, basestring):
        name = '%s://%s' % (protocol, name)
    if isinstance(port, int):
        name = '%s:%s' % (domain, port)
    return name.lower()

@swallow_args
def unicode_to_str(value):
    return value.encode('utf-8')


def camel_case_split(value, char='-', lower=True, upper=True):
    value = rx_camel_case_split.sub(r'%s\1' % char, value)
    if lower:
        value = value.lower()
    elif upper:
        value = value.upper()
    return value


def safe_str_cmp(one, two):
    if isinstance(one, unicode):
        one = unicode_to_str(one)
    if isinstance(two, unicode):
        two = unicode_to_str(one)
    if len(one) != len(two):
        return False
    rv = 0
    for x, y in izip(one, two):
        rv |= ord(x) ^ ord(y)
    return rv == 0


@swallow_args
def str_to_bool(value):
    value = value.lower()
    if value in ('true', 'si', 'oui', 'yes'):
        return True
    elif value in ('false', 'no', 'non'):
        return False
    return None


def _strptime(value, strptime_format):
    split_value = value.split('.')
    datetime_obj = datetime.datetime.strptime(split_value[0], strptime_format)
    if len(split_value) == 2:
        datetime_obj = datetime_obj.replace(microsecond=int(split_value[1]))
    return datetime_obj


@swallow_args
def str_to_date(value):
    return _strptime(value, '%Y-%m-%d').date()


@swallow_args
def str_to_time(value):
    return _strptime(value, '%H:%M:%S').time()


@swallow_args
def str_to_datetime(value):
    return _strptime(value, '%Y-%m-%d %H:%M:%S')


def week_range(value=None):
    if not isinstance(value, datetime.date):
        value = datetime.date.today()
    value = datetime.datetime(value.year, value.month, value.day)
    year, week, dow = value.isocalendar()
    ws = value if dow == 7 else value - datetime.timedelta(dow)
    we = ws + datetime.timedelta(6)
    return ws, we


def datetime_parser(value, default=None):
    kwargs = {}
    if isinstance(value, (datetime.date, datetime.time, datetime.datetime,
                          datetime.timedelta)):
        return value
    elif isinstance(value, (tuple, list)):
        value = ' '.join([str(x) for x in value])
    elif isinstance(value, int):
        value = str(value)
    elif isinstance(value, dict):
        kwargs = value
        value = kwargs.pop('date')
    try:
        try:
            date = dateutil.parser.parse(value, **kwargs)
        except ValueError:
            date = dateutil.parser.parse(value, fuzzy=True, **kwargs)
        return date
    except:
        return default or datetime.datetime.utcnow()


@swallow_args
def complex_types(value):
    if isinstance(value, unicode):
        return unicode_to_str(value)
    elif is_primitive(value):
        return value
    elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        return value.isoformat()
    return str(value)


@swallow_args
def serialize_complex_types(value):
    if hasattr(value, 'iteritems') or hasattr(value, 'items'):
        return dict(((k, complex_types(v)) for k, v in value.iteritems()))
    elif hasattr(value, '__iter__') and not isinstance(value, (str, unicode)):
        return list((complex_types(v) for v in value))
    return complex_types(value)


@swallow_args
def parser_types(value):
    try:
        value_str = str(value)
    except UnicodeEncodeError:
        value_str = unicode_to_str(value)
    if rx_isoformat_date.search(value_str):
        return str_to_date(value_str)
    elif rx_isoformat_time.search(value_str):
        return str_to_time(value_str)
    elif rx_isoformat.search(value_str):
        return datetime_parser(value_str)
    elif value_str.lower() in ('true', 'oui', 'yes', 'si', 'y'):
        return True
    elif value_str.lower() in ('false', 'no', 'not', 'n'):
        return False
    return value


@swallow_args
def deserialize_complex_types(value):
    if hasattr(value, 'iteritems') or hasattr(value, 'items'):
        return dict(((k, parser_types(v)) for k, v in value.iteritems()))
    elif hasattr(value, '__iter__') and not isinstance(value, (str, unicode)):
        return list((parser_types(v) for v in value))
    return parser_types(value)


def trace_error(data):
    logging.error(traceback.format_exc())
    if isinstance(data, (tuple, list, dict,)):
        logging.error(json.dumps(data, default=complex_types, indent=2))
    else:
        print data


def abspath(path, root=None):
    if root is not None:
        path = os.path.join(root, path)
    return os.path.abspath(path)


def verify_folder_list(*folders):
    for folder_path in folders:
        if not isinstance(folder_path, basestring):
            raise ValueError('Folder path must be a basestring')
        if not os.path.isdir(folder_path):
            raise ConfigurationError('Folder not found: %s' % folder_path)


def verify_folder(folder_name, root=None):
    folder_name = abspath(folder_name, root)
    verify_folder_list(folder_name)
    return folder_name


def verify_file_list(*files):
    for file_path in files:
        if not isinstance(file_path, basestring):
            raise ValueError('File path must be a basestring')
        if not os.path.isfile(file_path):
            raise ConfigurationError('File not found: %s' % file_path)


def verify_file(file_name, root=None):
    file_name = abspath(file_name, root)
    verify_file_list(file_name)
    return file_name


def verify_settings(settings, values=None):
    result = dict()
    for key in values:
        if key not in settings:
            raise KeyError('Key not supported: %s' % key)
        value = settings[key]
        if isinstance(value, (list, tuple, dict, set,)):
            value = copy.deepcopy(value)
        result[key] = value
    return result


def purge_settings(settings, values=None):
    if not values:
        return settings
    result = dict()
    for key in settings:
        if key not in values:
            continue
        value = settings[key]
        if isinstance(value, (list, tuple, dict, set,)):
            value = copy.deepcopy(value)
        result[key] = value
    return result


def import_by_path(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ConfigurationError(
            '%s doesn\'t look like a module path' % dotted_path)
    try:
        module = import_module(module_path)
    except ImportError, e:
        raise ConfigurationError(
            'Error importing module %s: %s' % (module_path, e))
    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ConfigurationError(
            'Module "%s" does not define a "%s" attribute/class' % (
                module_path, class_name))
    return attr
