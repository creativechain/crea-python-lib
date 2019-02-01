from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from crea import Crea
from crea.witness import Witness, Witnesses, WitnessesVotedByAccount, WitnessesRankedByVote
from crea.instance import set_shared_crea_instance
from crea.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.bts = Crea(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            unsigned=True,
            keys={"active": wif},
            num_retries=10
        )
        cls.creait = Crea(
            node="https://node1.creary.net",
            nobroadcast=True,
            unsigned=True,
            keys={"active": wif},
            num_retries=10
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_crea_instance(cls.bts)
        cls.bts.set_default_account("test")

    @parameterized.expand([
        ("normal"),
        ("creait"),
    ])
    def test_feed_publish(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.creait
        bts.txbuffer.clear()
        w = Witness("gtg", crea_instance=bts)
        tx = w.feed_publish("4 CBD", "1 CREA")
        self.assertEqual(
            (tx["operations"][0][0]),
            "feed_publish"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "gtg",
            op["publisher"])

    @parameterized.expand([
        ("normal"),
        ("creait"),
    ])
    def test_update(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.creait
        bts.txbuffer.clear()
        w = Witness("gtg", crea_instance=bts)
        props = {"account_creation_fee": "0.1 CREA",
                 "maximum_block_size": 32000,
                 "sbd_interest_rate": 0}
        tx = w.update(wif, "", props)
        self.assertEqual((tx["operations"][0][0]), "witness_update")
        op = tx["operations"][0][1]
        self.assertIn(
            "gtg",
            op["owner"])

    @parameterized.expand([
        ("normal"),
        ("creait"),
    ])
    def test_witnesses(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.creait
        w = Witnesses(crea_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("normal"),
        ("creait"),
    ])
    def test_WitnessesVotedByAccount(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.creait
        w = WitnessesVotedByAccount("gtg", crea_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("normal"),
        ("creait"),
    ])
    def test_WitnessesRankedByVote(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.creait
        w = WitnessesRankedByVote(crea_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("normal"),
        ("creait"),
    ])
    def test_export(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.creait
        owner = "gtg"
        if bts.rpc.get_use_appbase():
            witness = bts.rpc.find_witnesses({'owners': [owner]}, api="database")['witnesses']
            if len(witness) > 0:
                witness = witness[0]
        else:
            witness = bts.rpc.get_witness_by_account(owner)

        w = Witness(owner, crea_instance=bts)
        keys = list(witness.keys())
        json_witness = w.json()
        exclude_list = ['votes', 'virtual_last_update', 'virtual_scheduled_time']
        for k in keys:
            if k not in exclude_list:
                if isinstance(witness[k], dict) and isinstance(json_witness[k], list):
                    self.assertEqual(list(witness[k].values()), json_witness[k])
                else:
                    self.assertEqual(witness[k], json_witness[k])
