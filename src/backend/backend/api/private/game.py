#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Licensed under the MIT License.
# Author: Alejandro M. Bernardis
# Email: alejandro (dot) bernardis (at) asumikamikaze (dot) com
# Created: 12/Oct/2014 19:42

from backend.api.base import BaseHandler
from backend.common.errors import SchemaError


class Handler(BaseHandler):
    _schema = None

    def get(self, *args, **kwargs):
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
    (r'/s/path/(?P<sid>[a-z0-9]+)/?', Handler)
]
