import unittest
from crea import Crea
from crea.account import Account
from crea.instance import set_shared_crea_instance, SharedInstance
from crea.blockchainobject import BlockchainObject
from crea.nodelist import NodeList

import logging
log = logging.getLogger()


class Testcases(unittest.TestCase):

    def test_stm1stm2(self):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        b1 = Crea(
            node="https://nodes.creary.net",
            nobroadcast=True,
            num_retries=10
        )
        node_list = nodelist.get_nodes(exclude_limited=True)

        b2 = Crea(
            node=node_list,
            nobroadcast=True,
            num_retries=10
        )

        self.assertNotEqual(b1.rpc.url, b2.rpc.url)

    def test_default_connection(self):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))

        b2 = Crea(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
        )
        set_shared_crea_instance(b2)
        bts = Account("crea")
        self.assertEqual(bts.crea.prefix, "STM")
