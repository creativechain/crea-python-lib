from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
from parameterized import parameterized
import random
import json
from pprint import pprint
from crea import Crea, exceptions
from crea.amount import Amount
from crea.memo import Memo
from crea.version import version as crea_version
from crea.wallet import Wallet
from crea.witness import Witness
from crea.account import Account
from creagraphenebase.account import PrivateKey
from crea.instance import set_shared_crea_instance
from crea.nodelist import NodeList
from crea.creaconnect import CreaConnect
# Py3 compatibility
import sys
core_unit = "STM"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.bts = Crea(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            unsigned=True,
            data_refresh_time_seconds=900,
            num_retries=10)

        cls.account = Account("test", full=True, crea_instance=cls.bts)

    def test_transfer(self):
        bts = self.bts
        acc = self.account
        acc.crea.txbuffer.clear()
        tx = acc.transfer(
            "test1", 1.000, "CREA", memo="test")
        sc2 = CreaConnect(crea_instance=bts)
        url = sc2.url_from_tx(tx)
        url_test = 'https://creaconnect.com/sign/transfer?from=test&to=test1&amount=1.000+CREA&memo=test'
        self.assertEqual(len(url), len(url_test))
        self.assertEqual(len(url.split('?')), 2)
        self.assertEqual(url.split('?')[0], url_test.split('?')[0])

        url_parts = (url.split('?')[1]).split('&')
        url_test_parts = (url_test.split('?')[1]).split('&')

        self.assertEqual(len(url_parts), 4)
        self.assertEqual(len(list(set(url_parts).intersection(set(url_test_parts)))), 4)

    def test_login_url(self):
        bts = self.bts
        sc2 = CreaConnect(crea_instance=bts)
        url = sc2.get_login_url("localhost", scope="login,vote")
        url_test = 'https://creaconnect.com/oauth2/authorize?client_id=None&redirect_uri=localhost&scope=login,vote'
        self.assertEqual(len(url), len(url_test))
        self.assertEqual(len(url.split('?')), 2)
        self.assertEqual(url.split('?')[0], url_test.split('?')[0])

        url_parts = (url.split('?')[1]).split('&')
        url_test_parts = (url_test.split('?')[1]).split('&')

        self.assertEqual(len(url_parts), 3)
        self.assertEqual(len(list(set(url_parts).intersection(set(url_test_parts)))), 3)
