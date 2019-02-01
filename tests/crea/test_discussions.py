from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from crea import Crea
from crea.discussions import (
    Query, Discussions_by_trending, Comment_discussions_by_payout,
    Post_discussions_by_payout, Discussions_by_created, Discussions_by_active,
    Discussions_by_cashout, Discussions_by_votes,
    Discussions_by_children, Discussions_by_hot, Discussions_by_feed, Discussions_by_blog,
    Discussions_by_comments, Discussions_by_promoted, Discussions
)
from datetime import datetime
from crea.instance import set_shared_crea_instance
from crea.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False, appbase=True), num_retries=10))
        node_list = nodelist.get_nodes(exclude_limited=True)
      
        cls.bts = Crea(
            node=node_list,
            use_condenser=True,
            nobroadcast=True,
            keys={"active": wif},
            num_retries=10
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_crea_instance(cls.bts)
        cls.bts.set_default_account("test")

    def test_trending(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "creait"
        d = Discussions_by_trending(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_comment_payout(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "creait"
        d = Comment_discussions_by_payout(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_post_payout(self):
        bts = self.bts

        query = Query()
        query["limit"] = 10
        query["tag"] = "creait"
        d = Post_discussions_by_payout(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_created(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "creait"
        d = Discussions_by_created(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_active(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "creait"
        d = Discussions_by_active(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_cashout(self):
        bts = self.bts
        query = Query(limit=10)
        Discussions_by_cashout(query, crea_instance=bts)
        # self.assertEqual(len(d), 10)

    def test_votes(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "creait"
        d = Discussions_by_votes(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_children(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "creait"
        d = Discussions_by_children(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_feed(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "gtg"
        d = Discussions_by_feed(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_blog(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "gtg"
        d = Discussions_by_blog(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_comments(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["filter_tags"] = ["gtg"]
        query["start_author"] = "gtg"
        d = Discussions_by_comments(query, crea_instance=bts)
        self.assertEqual(len(d), 10)

    def test_promoted(self):
        bts = self.bts
        query = Query()
        query["limit"] = 10
        query["tag"] = "creait"
        d = Discussions_by_promoted(query, crea_instance=bts)
        discussions = Discussions(crea_instance=bts)
        d2 = []
        for dd in discussions.get_discussions("promoted", query, limit=10):
            d2.append(dd)
        self.assertEqual(len(d), 10)
        self.assertEqual(len(d2), 10)
