from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
import mock
import pytz
from datetime import datetime, timedelta
from parameterized import parameterized
from pprint import pprint
from crea import Crea, exceptions, constants
from crea.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.appbase = Crea(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            bundle=False,
            # Overwrite wallet to use this list of wifs only
            keys={"active": wif},
            num_retries=10
        )

    def test_constants(self):
        stm = self.appbase
        crea_conf = stm.get_config()
        if "CREA_100_PERCENT" in crea_conf:
            CREA_100_PERCENT = crea_conf['CREA_100_PERCENT']
        else:
            CREA_100_PERCENT = crea_conf['CREARY_100_PERCENT']
        self.assertEqual(constants.CREA_100_PERCENT, CREA_100_PERCENT)

        if "CREA_1_PERCENT" in crea_conf:
            CREA_1_PERCENT = crea_conf['CREA_1_PERCENT']
        else:
            CREA_1_PERCENT = crea_conf['CREARY_1_PERCENT']
        self.assertEqual(constants.CREA_1_PERCENT, CREA_1_PERCENT)

        if "CREA_REVERSE_AUCTION_WINDOW_SECONDS" in crea_conf:
            CREA_REVERSE_AUCTION_WINDOW_SECONDS = crea_conf['CREA_REVERSE_AUCTION_WINDOW_SECONDS']
        elif "CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF6" in crea_conf:
            CREA_REVERSE_AUCTION_WINDOW_SECONDS = crea_conf['CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF6']
        else:
            CREA_REVERSE_AUCTION_WINDOW_SECONDS = crea_conf['CREARY_REVERSE_AUCTION_WINDOW_SECONDS']
        self.assertEqual(constants.CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF6, CREA_REVERSE_AUCTION_WINDOW_SECONDS)

        if "CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF20" in crea_conf:
            self.assertEqual(constants.CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF20, crea_conf["CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF20"])

        if "CREA_VOTE_DUST_THRESHOLD" in crea_conf:
            self.assertEqual(constants.CREA_VOTE_DUST_THRESHOLD, crea_conf["CREA_VOTE_DUST_THRESHOLD"])

        if "CREA_VOTE_REGENERATION_SECONDS" in crea_conf:
            CREA_VOTE_REGENERATION_SECONDS = crea_conf['CREA_VOTE_REGENERATION_SECONDS']
            self.assertEqual(constants.CREA_VOTE_REGENERATION_SECONDS, CREA_VOTE_REGENERATION_SECONDS)
        elif "CREA_VOTING_MANA_REGENERATION_SECONDS" in crea_conf:
            CREA_VOTING_MANA_REGENERATION_SECONDS = crea_conf["CREA_VOTING_MANA_REGENERATION_SECONDS"]
            self.assertEqual(constants.CREA_VOTING_MANA_REGENERATION_SECONDS, CREA_VOTING_MANA_REGENERATION_SECONDS)
        else:
            CREA_VOTE_REGENERATION_SECONDS = crea_conf['CREARY_VOTE_REGENERATION_SECONDS']
            self.assertEqual(constants.CREA_VOTE_REGENERATION_SECONDS, CREA_VOTE_REGENERATION_SECONDS)

        if "CREA_ROOT_POST_PARENT" in crea_conf:
            CREA_ROOT_POST_PARENT = crea_conf['CREA_ROOT_POST_PARENT']
        else:
            CREA_ROOT_POST_PARENT = crea_conf['CREARY_ROOT_POST_PARENT']
        self.assertEqual(constants.CREA_ROOT_POST_PARENT, CREA_ROOT_POST_PARENT)
