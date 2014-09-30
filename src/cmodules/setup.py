#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 25/Sep/2014 9:23 PM

import os
import shutil
from distutils.core import setup, Extension

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
BUILD_PATH = os.path.join(ROOT_PATH, "build")

if os.path.isdir(BUILD_PATH):
    shutil.rmtree(BUILD_PATH)

setup(
    name="backend",
    # TODO: *** Remember to change the version ***
    version="1.0.0.dev.0",
    packages = ["backend", "backend.games"],
    author="Alejandro M. Bernardis",
    author_email="alejandro (dot) bernardis (at) asumikamikaze (dot) com",
    url="http://https://github.com/alejandrobernardis/python-slot-machines/",
    license="https://raw.githubusercontent.com/alejandrobernardis"
            "/python-slot-machines/master/LICENSE",
    description="This is a pilot project that provides a backend written in "
                "python for a mobile gaming platform.",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    ext_modules=[
        Extension(
            "backend.games._find_golden_eggs",
            ["backend/games/_find_golden_eggs.c"]
        ),
        Extension(
            "backend.games._roulettes",
            ["backend/games/_roulettes.c"]
        ),
        Extension(
            "backend.games._slots",
            ["backend/games/_slots.c"]
        )
    ]
)
