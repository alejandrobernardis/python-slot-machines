#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 31/07/2013 18:05

import re

SEPARATOR = '|'
VALIDATE_HASH = re.compile(r'^I(\d)+$')
VALIDATE_KEY = re.compile(r'^I(\d)+\|[a-zA-Z0-9-]+$')
VALIDATE_TOKEN = re.compile(r'^\^[\d]{4,}\/[\d]{2,}\/[\d]{2,}\|'
                            r'[\d]{2,}:[\d]{2,}:[\d]{2,}\.[\d]{1,4}\|'
                            r'domain\.tld\|'
                            r'[a-zA-Z0-9]{6,}\$$')

VALIDATE_INDEX = re.compile(r'\d')
VALIDATE_LETTERS = re.compile(r'[a-z]', re.I)
LETTERS_MIN = 'abcdefghijklmnopqrstuvwxyz'
LETTERS_MAY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS = LETTERS_MIN+LETTERS_MAY
LETTERS_LEN = len(LETTERS)-1

SECRET_HASH = ''

# ------------------------------------------------------------------------------

KEYS = ''

# ------------------------------------------------------------------------------


class IronMan(object):
    @staticmethod
    def doit(literal, key):
        result = u''
        key_index = 0
        for i in literal:
            number = ord(i) ^ ord(key[key_index])
            xored = str(number)
            if number < 10:
                xored = '00' + xored
            elif number < 100:
                xored = '0' + xored
            result += xored
            if key_index == len(key)-1:
                key_index = 0
            else:
                key_index += 1
        return result

    @staticmethod
    def rdoit(literal, key):
        result = u''
        key_index = 0
        key_coef = 3
        for i in xrange(0, len(literal)/key_coef):
            pos = i * key_coef
            xored = int(literal[pos:pos+key_coef])
            result += chr(xored ^ ord(key[key_index]))
            if key_index == len(key)-1:
                key_index = 0
            else:
                key_index += 1
        return result

    @staticmethod
    def defense(value):
        if not VALIDATE_HASH.match(value):
            raise ValueError(u'El formato del request no es correcto.')
        value = IronMan.rdoit(value[1:], SECRET_HASH)
        if not VALIDATE_KEY.match(value):
            raise ValueError(u'El formato de la clave no es correcto.')
        value = value.split(SEPARATOR)
        result = IronMan.rdoit(value[0][1:], value[1])
        if not VALIDATE_TOKEN.match(result):
            raise ValueError(u'El formato del literal no es correcto.')
        result = result[1:-1].split(SEPARATOR)
        if len(result) is not 4:
            raise ValueError(u'La cantidad de bloques no es correcta.')
        super_key = result[3]
        index = int(VALIDATE_INDEX.findall(super_key)[0])
        letters = VALIDATE_LETTERS.findall(super_key)
        result = u''
        for i in letters:
            new_index = LETTERS.index(i)+index
            if new_index <= LETTERS_LEN:
                result += LETTERS[new_index]
            else:
                result += LETTERS[(new_index-LETTERS_LEN)-1]
        result += str(index)
        return result in KEYS