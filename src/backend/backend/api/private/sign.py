#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 07/Oct/2014 7:23 PM

from backend.api.base import BaseHandler
from backend.common.errors import SchemaError
from backend.models.requests.services import SignIn, SignOut


class SignInHandler(BaseHandler):
    _schema = SignIn

    def get(self, uid, *args, **kwargs):
        """ New User """
        try:
            schema, validate = self.validate_schema()

            if not validate:
                raise SchemaError(schema.errors)

            self.get_json_response_and_finish()

        except SchemaError, e:
            self.get_json_error_response_and_finish(e)

        except Exception, e:
            self.get_json_exception_response_and_finish(e)

    def put(self, uid, *args, **kwargs):
        """ Old User """
        try:
            schema, validate = self.validate_schema()
            if not validate:
                raise SchemaError(schema.errors)
            self.get_json_response_and_finish()
        except SchemaError, e:
            self.get_json_error_response_and_finish(e)
        except Exception, e:
            self.get_json_exception_response_and_finish(e)


class SignOutHandler(BaseHandler):
    _schema = SignOut

    def delete(self, sid, *args, **kwargs):
        try:
            schema, validate = self.validate_schema()
            if not validate:
                raise SchemaError(schema.errors)
            self.get_json_response_and_finish()
        except SchemaError, e:
            self.get_json_error_response_and_finish(e)
        except Exception, e:
            self.get_json_exception_response_and_finish(e)


handlers_list = [
    (r'/s/sign/in(?P<uid>\/[a-z0-9]+)?/?', SignInHandler),
    (r'/s/sign/out/(?P<sid>[a-z0-9]+)/?', SignOutHandler)
]
