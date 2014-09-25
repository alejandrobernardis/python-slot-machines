#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 24/Sep/2014 4:01 AM

from functools import wraps

try:
    from werkzeug.security import generate_password_hash
except ImportError:
    generate_password_hash = None

try:
    from werkzeug.security import check_password_hash
except ImportError:
    check_password_hash = None

__all__ = (
    'validate_password',
    'SHA1Password',
    'SHA256Password',
    'SHA512Password',
    'MD5Password'
)


MAXIMUM_PASSWORD_LENGTH = 4096
MINIMUM_PASSWORD_LENGTH = 8


def validate_password(length):
    def inner(fn):
        @wraps(fn)
        def wrapper(self, password, *args, **kwargs):
            password_len = len(password)
            if password_len < length or password_len > MAXIMUM_PASSWORD_LENGTH:
                raise ValueError(
                    'Invalid password, must be greater than or equal to %s'
                    % length
                )
            return fn(self, password, *args, **kwargs)
        return wrapper
    return inner


class _PasswordHasher(object):
    _algorithm = None

    @validate_password(MINIMUM_PASSWORD_LENGTH)
    def make(self, password, salt=None):
        if not generate_password_hash:
            raise ImportError('Function `generate_password_hash` not found')
        if not isinstance(salt, int):
            salt = 8
        return generate_password_hash(password, self._algorithm, salt)

    @validate_password(MINIMUM_PASSWORD_LENGTH)
    def verify(self, password, password_hash):
        if not check_password_hash:
            raise ImportError('Function `check_password_hash` not found')
        return check_password_hash(password, password_hash)


class SHA1Password(_PasswordHasher):
    _algorithm = 'pbkdf2:sha1'


class SHA256Password(_PasswordHasher):
    _algorithm = 'pbkdf2:sha256'


class SHA512Password(_PasswordHasher):
    _algorithm = 'pbkdf2:sha512'


class MD5Password(_PasswordHasher):
    _algorithm = 'pbkdf2:md5'