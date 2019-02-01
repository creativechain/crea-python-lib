from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
import random
from parameterized import parameterized
from pprint import pprint
from crea import Crea
from crea.amount import Amount
from crea.witness import Witness
from crea.account import Account
from crea.instance import set_shared_crea_instance, shared_crea_instance, set_shared_config
from crea.blockchain import Blockchain
from crea.block import Block
from crea.market import Market
from crea.price import Price
from crea.comment import Comment
from crea.vote import Vote
from creaapi.exceptions import RPCConnection
from crea.wallet import Wallet
from crea.transactionbuilder import TransactionBuilder
from creabase.operations import Transfer
from creagraphenebase.account import PasswordKey, PrivateKey, PublicKey
from crea.utils import parse_time, formatTimedelta
from crea.nodelist import NodeList

# Py3 compatibility
import sys

core_unit = "STM"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodelist = NodeList()
        cls.nodelist.update_nodes(crea_instance=Crea(node=cls.nodelist.get_nodes(exclude_limited=False), num_retries=10))
        stm = Crea(node=cls.nodelist.get_nodes())
        stm.config.refreshBackup()
        stm.set_default_nodes(["xyz"])
        del stm

        cls.urls = cls.nodelist.get_nodes(exclude_limited=True)
        cls.bts = Crea(
            node=cls.urls,
            nobroadcast=True,
            num_retries=10
        )
        set_shared_crea_instance(cls.bts)
        acc = Account("holger80", crea_instance=cls.bts)
        comment = acc.get_blog(limit=20)[-1]
        cls.authorperm = comment.authorperm
        votes = acc.get_account_votes()
        last_vote = votes[-1]
        cls.authorpermvoter = '@' + last_vote['authorperm'] + '|' + acc["name"]

    @classmethod
    def tearDownClass(cls):
        stm = Crea(node=cls.nodelist.get_nodes())
        stm.config.recover_with_latest_backup()

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_account(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            acc = Account("test")
            self.assertIn(acc.crea.rpc.url, self.urls)
            self.assertIn(acc["balance"].crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test", crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            acc = Account("test", crea_instance=stm)
            self.assertIn(acc.crea.rpc.url, self.urls)
            self.assertIn(acc["balance"].crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test")

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_amount(self, node_param):
        if node_param == "instance":
            stm = Crea(node="https://abc.d", autoconnect=False, num_retries=1)
            set_shared_crea_instance(self.bts)
            o = Amount("1 CBD")
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 CBD", crea_instance=stm)
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Amount("1 CBD", crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 CBD")

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_block(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Block(1)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1, crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Block(1, crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1)

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_blockchain(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Blockchain()
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain(crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Blockchain(crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain()

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_comment(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Comment(self.authorperm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm, crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Comment(self.authorperm, crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm)

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_market(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Market()
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market(crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Market(crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market()

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_price(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Price(10.0, "CREA/CBD")
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "CREA/CBD", crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Price(10.0, "CREA/CBD", crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "CREA/CBD")

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_vote(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Vote(self.authorpermvoter)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter, crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Vote(self.authorpermvoter, crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter)

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_wallet(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Wallet()
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet(crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
                o.crea.get_config()
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Wallet(crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet()
                o.crea.get_config()

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_witness(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Witness("gtg")
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg", crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Witness("gtg", crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg")

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_transactionbuilder(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = TransactionBuilder()
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder(crea_instance=Crea(node="https://abc.d", autoconnect=False, num_retries=1))
                o.crea.get_config()
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = TransactionBuilder(crea_instance=stm)
            self.assertIn(o.crea.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder()
                o.crea.get_config()

    @parameterized.expand([
        ("instance"),
        ("crea")
    ])
    def test_crea(self, node_param):
        if node_param == "instance":
            set_shared_crea_instance(self.bts)
            o = Crea(node=self.urls)
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                stm = Crea(node="https://abc.d", autoconnect=False, num_retries=1)
                stm.get_config()
        else:
            set_shared_crea_instance(Crea(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = stm
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                stm = shared_crea_instance()
                stm.get_config()

    def test_config(self):
        set_shared_config({"node": self.urls})
        set_shared_crea_instance(None)
        o = shared_crea_instance()
        self.assertIn(o.rpc.url, self.urls)
