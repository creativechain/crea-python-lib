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
from crea import Crea
from crea.amount import Amount
from crea.memo import Memo
from crea.version import version as crea_version
from crea.wallet import Wallet
from crea.witness import Witness
from crea.account import Account
from creagraphenebase.account import PrivateKey
from crea.instance import set_shared_crea_instance, shared_crea_instance
from crea.nodelist import NodeList
# Py3 compatibility
import sys
core_unit = "STM"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        stm = shared_crea_instance()
        stm.config.refreshBackup()
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))

        cls.stm = Crea(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            # We want to bundle many operations into a single transaction
            bundle=True,
            num_retries=10
            # Overwrite wallet to use this list of wifs only
        )

        cls.stm.set_default_account("test")
        set_shared_crea_instance(cls.stm)
        # self.stm.newWallet("TestingOneTwoThree")

        cls.wallet = Wallet(crea_instance=cls.stm)
        cls.wallet.wipe(True)
        cls.wallet.newWallet(pwd="TestingOneTwoThree")
        cls.wallet.unlock(pwd="TestingOneTwoThree")
        cls.wallet.addPrivateKey(wif)

    @classmethod
    def tearDownClass(cls):
        stm = shared_crea_instance()
        stm.config.recover_with_latest_backup()

    def test_set_default_account(self):
        stm = self.stm
        stm.set_default_account("creabot")

        self.assertEqual(stm.config["default_account"], "creabot")
