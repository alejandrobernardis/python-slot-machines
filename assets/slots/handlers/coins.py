#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 19/08/2013 17:03

import re
import json
import base64
from celery_tasks import push_store_activity
from  slots.common.utils import str_to_int
from  slots.handlers.base import BaseHandler
from  slots.security.sessions import session_verify
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


environment_type = re.compile(r'"environment"\s=\s"sandbox";', re.I)


BUYING_COINS_TABLE = {
    "version": 1.0,
    "modified": "0000-00-00 00:00:00",
    "store": {
        "pack_0001": {
            "coinsa": "0",
            "gratis": "0%",
            "coinsb": "0",
            "money": "0,00 USD"
        }
    }
}


BUYING_COINS_IDS = (
    "pack_0001"
)



APPLE_URL_LIVE = 'https://buy.itunes.apple.com/verifyReceipt'
APPLE_URL_SANDBOX = 'https://sandbox.itunes.apple.com/verifyReceipt'

APPLE_ERROR = {
    21000: 'The App Store could not read the JSON object you provided.',
    21002: 'The data in the receipt-data property was malformed.',
    21003: 'The receipt could not be authenticated.',
    21004: 'The shared secret you provided does not match the shared secret '
           'on file for your account.',
    21005: 'The receipt server is not currently available.',
    21006: 'This receipt is valid but the subscription has expired. When this '
           'status code is returned to your server, the receipt data is also '
           'decoded and returned as part of the response.',
    21007: 'This receipt is a sandbox receipt, but it was sent to the '
           'production service for verification.',
    21008: 'This receipt is a production receipt, but it was sent to the '
           'sandbox service for verification.',
}


class AddCoinsHandler(BaseHandler):
    _client = AsyncHTTPClient()

    @session_verify
    @asynchronous
    @gen.coroutine
    def post(self):
        debug = self.settings.get('debug', False)
        in_approval = self.settings.get('in_approval', False)
        receipt = self.get_argument('receipt', None)
        product_id = self.get_argument('product_id', None)
        transaction_id = self.get_argument('transaction_id', None)
        coins = self.get_argument('coins', None)
        session = self.session.data
        try:
            self.validate_arguments(
                receipt, product_id, transaction_id, coins
            )
            data_track = self.db_track['activity.store']
            if data_track.find_one({'transaction_id': transaction_id}):
                raise ValueError(
                    'Transaction id duplicate: %s ' % transaction_id
                )
            sandbox = bool(environment_type.search(receipt))
            if sandbox and in_approval or debug:
                activity = 'add_coins_success_for_review'
                url = APPLE_URL_SANDBOX
            else:
                activity = 'add_coins_success'
                url = APPLE_URL_LIVE
            _req = HTTPRequest(url)
            _req.method = 'POST'
            _req.headers = {'Content-Type': 'text/json; charset=utf-8'}
            _req.body = json.dumps({'receipt-data': base64.b64encode(receipt)})
            _task = yield gen.Task(self._client.fetch, _req)
            _response = json.loads(_task.body)
            status = _response.get('status')
            if status and status in APPLE_ERROR:
                raise Exception('(%s) %s' % (status, APPLE_ERROR.get(status)))
            verify = _response.get('receipt')
            if verify.get('error'):
                raise ValueError(verify['error'].get('message'))
            elif product_id != verify.get('product_id'):
                raise ValueError('Product ID (x)')
            elif transaction_id != verify.get('transaction_id'):
                raise ValueError('Receipt ID (x)')
            pack_value = BUYING_COINS_TABLE.get('store').get(product_id, None)
            if not pack_value:
                raise ValueError('Pack Value (x)')
            pack_pay = str_to_int(pack_value, 'coinsa')
            pack_bonus = str_to_int(pack_value, 'coinsb')
            session_balance = float(session.get('balance', 0))
            if pack_pay != str_to_int(coins):
                raise ValueError('Pack Pay (?)')
            balance = float(session_balance + (pack_bonus or pack_pay))
            session.update(balance=balance)
            self.verify_user_config(session)
            try:
                if self.settings.get('track', True):
                    push_store_activity.delay(
                        uid=session.get('uid'),
                        sid=session.get('sid'),
                        fbuid=session.get('fbuid', None),
                        activity=activity,
                        receipt=receipt,
                        balance=balance,
                        sandbox=sandbox,
                        debug=debug,
                        in_approval=in_approval,
                        **verify
                    )
            except Exception:
                pass
            self.get_json_response_and_finish(
                response={
                    'balance': balance
                }
            )
        except Exception, e:
            try:
                if self.settings.get('track', True):
                    push_store_activity.delay(
                        uid=session.get('uid'),
                        sid=session.get('sid'),
                        fbuid=session.get('fbuid', None),
                        activity='add_coins_error',
                        error='(e): %s' % e,
                        receipt=receipt,
                        product_id=product_id,
                        transaction_id=transaction_id,
                        coins=coins,
                        sandbox=bool(environment_type.search(receipt)),
                        debug=debug,
                        in_approval=in_approval
                    )
            except Exception:
                pass
            self.get_except_json_response_and_finish(e)


PUBLIC_KEY = ''

VERIFY_KEY = RSA.importKey(base64.decodestring(PUBLIC_KEY))
PACKAGE_NAME = 'tld.domain.Android'


class AndroidAddCoinsHandler(BaseHandler):

    @session_verify
    def post(self):
        receipt = self.get_argument('receipt', None)
        signature = self.get_argument('signature', None)
        coins = self.get_argument('coins', None)
        session = self.session.data
        try:
            self.validate_arguments(receipt, signature)
            receipt_object = json.loads(receipt)
            package_name = receipt_object.get('packageName')
            if package_name != PACKAGE_NAME:
                raise ValueError('Package Name (x)')
            product_id = receipt_object.get('productId')
            if product_id not in BUYING_COINS_IDS:
                raise ValueError('Product ID')
            transaction_id = receipt_object.get('orderId')
            if not transaction_id:
                raise ValueError('Transaction ID (?)')
            data_track = self.db_track['activity.store']
            if data_track.find_one({'transaction_id': transaction_id}):
                raise ValueError('Transaction ID (x)')
            h = SHA.new(receipt)
            verifier = PKCS1_v1_5.new(VERIFY_KEY)
            signature_decode = base64.decodestring(signature)
            if not verifier.verify(h, signature_decode):
                raise ValueError('Transaction (x)')
            pack_value = BUYING_COINS_TABLE.get('store').get(product_id, None)
            if not pack_value:
                raise ValueError('Pack Value (x)')
            pack_pay = str_to_int(pack_value, 'coinsa')
            pack_bonus = str_to_int(pack_value, 'coinsb')
            session_balance = float(session.get('balance', 0))
            if pack_pay != str_to_int(coins):
                raise ValueError('Pack Pay (?)')
            balance = float(session_balance + (pack_bonus or pack_pay))
            session.update(balance=balance)
            self.verify_user_config(session)
            try:
                if self.settings.get('track', True):
                    push_store_activity.delay(
                        uid=session.get('uid'),
                        sid=session.get('sid'),
                        fbuid=session.get('fbuid', None),
                        activity='add_coins_success',
                        receipt=receipt,
                        signature=signature,
                        coins=coins,
                        balance=balance,
                    )
            except Exception:
                pass
            return self.get_json_response_and_finish(
                response={
                    'balance': balance
                }
            )
        except Exception, e:
            try:
                if self.settings.get('track', True):
                    push_store_activity.delay(
                        uid=session.get('uid'),
                        sid=session.get('sid'),
                        fbuid=session.get('fbuid', None),
                        activity='add_coins_error',
                        error='(e): %s' % e,
                        receipt=receipt,
                        signature=signature,
                        coins=coins,
                    )
            except Exception:
                pass
            return self.get_except_json_response_and_finish(e)


handlers_list = [
    (r'/do/coins/add/?', AddCoinsHandler),
    (r'/do/coins/android/add/?', AndroidAddCoinsHandler),
]
