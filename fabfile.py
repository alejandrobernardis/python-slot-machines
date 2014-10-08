#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 08/Oct/2014 10:22 AM

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
LIBRARY_PATH = os.path.join(ROOT_PATH, '/Volumes/Projects/library/python/2.7')
DATA_LIB_PATH = os.path.join(ROOT_PATH, 'lib')
DATA_SRC_PATH = os.path.join(ROOT_PATH, 'src/backend')
PYTHON_PATH = '$PYTHONPATH:%s:%s:%s' \
              % (LIBRARY_PATH, DATA_LIB_PATH, DATA_SRC_PATH)

sys.path.append(LIBRARY_PATH)
sys.path.append(DATA_LIB_PATH)

from fabric.api import *


def _start(background=False, port=8000):
    with lcd(DATA_SRC_PATH):
        with shell_env(PYTHONPATH=PYTHON_PATH):
            command = 'python2.7 -m server --port=%s' % port
            if background:
                command = "nohup {0} > /tmp/backend.{1}.log 2>&1 " \
                          "& echo $! > /tmp/backend.{1}.pid" \
                          .format(command, port)
            local(command)


def _stop(port=8000):
    pid = open('/tmp/backend.%s.pid' % port).read().replace('\n', '')
    local('kill -9 %s %s' % (pid, int(pid)+1))


def _tail(port=8000):
    local('tail -f /tmp/backend.%s.log' % port)


@task
def start_backend(background=False):
    _start(background, 8000)


@task
def start_backend_api(background=False):
    _start(background, 9000)


@task
def start_all():
    start_backend(True)
    start_backend_api(True)


@task
def stop_backend():
    _stop(8000)


@task
def stop_backend_api():
    _stop(9000)


@task
def stop_all():
    stop_backend()
    stop_backend_api()


@task
def tail_backend():
    _tail(8000)


@task
def tail_backend_api():
    _tail(9000)


@task
def tail_all():
    tail_backend()
    tail_backend_api()
