#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 08/Oct/2014 10:22 AM

import os
import re
from fabric.api import *

rx_pid = re.compile(r'\d+')
BACKEND_PORT = 8000
BACKEND_API_PORT = 9000
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
LIBRARY_PATH = os.path.join(ROOT_PATH, '/Volumes/Projects/library/python/2.7')
DATA_LIB_PATH = os.path.join(ROOT_PATH, 'lib')
DATA_SRC_PATH = os.path.join(ROOT_PATH, 'src/backend')
PYTHON_PATH = '$PYTHONPATH:%s:%s:%s' \
              % (LIBRARY_PATH, DATA_LIB_PATH, DATA_SRC_PATH)


def _start_server(background=False, port=BACKEND_PORT):
    with lcd(DATA_SRC_PATH):
        with shell_env(PYTHONPATH=PYTHON_PATH):
            command = 'python2.7 -m server --port=%s' % port
            if background:
                command = "nohup {command} > /tmp/backend.{port}.log 2>&1 " \
                          "& echo $! > /tmp/backend.{port}.pid" \
                          .format(command=command, port=port)
            local(command)


def _stop_server(port=BACKEND_PORT):
    pid = rx_pid.findall(open('/tmp/backend.%s.pid' % port).read())[0]
    local('kill %s %s' % (pid, int(pid)+1))


def _tail_server(port=BACKEND_PORT):
    local('tail -f /tmp/backend.%s.log' % port)


def _start_db():
    config_file = os.path.join(ROOT_PATH, 'etc/mongodb.conf')
    path_dir = '/tmp/mongodb'
    if not os.path.isdir(path):
        local('mkdir -p {path}'.format(path=path_dir))
    local('mongod --config {config_file}'.format(config_file=config_file))


def _stop_db():
    pid = rx_pid.findall(open('/tmp/mongodb.pid').read())[0]
    local('kill {pid}'.format(pid=pid))


def _start_celery(background=False, worker='backend.background.server',
                  level='info'):
    with lcd(DATA_SRC_PATH):
        with shell_env(PYTHONPATH=PYTHON_PATH):
            command = 'celery -A {worker} worker --loglevel={level}' \
                      .format(worker=worker, level=level)
            if background:
                command = "nohup {command} > /tmp/celery.{worker}.log 2>&1 " \
                          "& echo $! > /tmp/celery.{worker}.pid" \
                          .format(command=command, worker=worker)
            local(command)


def _stop_celery(worker='backend.background.server'):
    pid = rx_pid.findall(open('/tmp/celery.{0}.pid'.format(worker)).read())[0]
    local('kill {pid}'.format(pid=pid))


def _start_broker(background=False, options=''):
    if background:
        options += ' -detached'
    local('rabbitmq-server{options}'.format(options=options))


def _stop_broker():
    pass


def _start_cache(server='memcached'):
    server = server.lower()
    if server not in ('redis', 'memcached'):
        raise ValueError('Server type not supported: %s' % server)
    if server == 'redis':
        config_file = os.path.join(ROOT_PATH, 'etc/redis.conf')
        path_dir = '/tmp/redis'
        if not os.path.isdir(path):
            local('mkdir -p {path}'.format(path=path_dir))
        local('redis-server {config_file}'.format(config_file=config_file))
    else:
        config_file = os.path.join(ROOT_PATH, 'etc/memcached.conf')
        local('memcached -d {config_file}'.format(config_file=config_file))


def _stop_cache(server='memcached'):
    server = server.lower()
    if server not in ('redis', 'memcached'):
        raise ValueError('Server type not supported: %s' % server)
    if server == 'redis':
        pid = rx_pid.findall(open('/tmp/redis.pid').read())[0]
        local('kill {pid}'.format(pid=pid))
    else:
        local('killall memcached')


# tasks ########################################################################

@task
def start_backend(background=False):
    _start_server(background)


@task
def stop_backend():
    _stop_server()


@task
def tail_backend():
    _tail_server()


@task
def start_backend_api(background=False):
    _start_server(background, BACKEND_API_PORT)


@task
def stop_backend_api():
    _stop_server(BACKEND_API_PORT)


@task
def tail_backend_api():
    _tail_server(BACKEND_API_PORT)


@task
def start_db():
    _start_db()


@task
def stop_db():
    _stop_db()