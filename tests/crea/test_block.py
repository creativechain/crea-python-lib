from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from crea import Crea, exceptions
from crea.block import Block, BlockHeader
from datetime import datetime
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
            keys={"active": wif},
            num_retries=10
        )
        cls.test_block_id = 19273700
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_crea_instance(cls.bts)
        cls.bts.set_default_account("test")

    def test_block(self):
        bts = self.bts
        test_block_id = self.test_block_id
        block = Block(test_block_id, crea_instance=bts)
        self.assertEqual(block.identifier, test_block_id)
        self.assertTrue(isinstance(block.time(), datetime))
        self.assertTrue(isinstance(block, dict))

        self.assertTrue(len(block.operations))
        self.assertTrue(isinstance(block.ops_statistics(), dict))

        block2 = Block(test_block_id + 1, crea_instance=bts)
        self.assertTrue(block2.time() > block.time())
        with self.assertRaises(
            exceptions.BlockDoesNotExistsException
        ):
            Block(0, crea_instance=bts)

    def test_block_only_ops(self):
        bts = self.bts
        test_block_id = self.test_block_id
        block = Block(test_block_id, only_ops=True, crea_instance=bts)
        self.assertEqual(block.identifier, test_block_id)
        self.assertTrue(isinstance(block.time(), datetime))
        self.assertTrue(isinstance(block, dict))

        self.assertTrue(len(block.operations))
        self.assertTrue(isinstance(block.ops_statistics(), dict))

        block2 = Block(test_block_id + 1, crea_instance=bts)
        self.assertTrue(block2.time() > block.time())
        with self.assertRaises(
            exceptions.BlockDoesNotExistsException
        ):
            Block(0, crea_instance=bts)

    def test_block_header(self):
        bts = self.bts
        test_block_id = self.test_block_id
        block = BlockHeader(test_block_id, crea_instance=bts)
        self.assertEqual(block.identifier, test_block_id)
        self.assertTrue(isinstance(block.time(), datetime))
        self.assertTrue(isinstance(block, dict))

        block2 = BlockHeader(test_block_id + 1, crea_instance=bts)
        self.assertTrue(block2.time() > block.time())
        with self.assertRaises(
            exceptions.BlockDoesNotExistsException
        ):
            BlockHeader(0, crea_instance=bts)

    def test_export(self):
        bts = self.bts
        block_num = 2000000

        if bts.rpc.get_use_appbase():
            block = bts.rpc.get_block({"block_num": block_num}, api="block")
            if block and "block" in block:
                block = block["block"]
        else:
            block = bts.rpc.get_block(block_num)

        b = Block(block_num, crea_instance=bts)
        keys = list(block.keys())
        json_content = b.json()

        for k in keys:
            if k not in "json_metadata":
                if isinstance(block[k], dict) and isinstance(json_content[k], list):
                    self.assertEqual(list(block[k].values()), json_content[k])
                else:
                    self.assertEqual(block[k], json_content[k])

        if bts.rpc.get_use_appbase():
            block = bts.rpc.get_block_header({"block_num": block_num}, api="block")
            if "header" in block:
                block = block["header"]
        else:
            block = bts.rpc.get_block_header(block_num)

        b = BlockHeader(block_num, crea_instance=bts)
        keys = list(block.keys())
        json_content = b.json()

        for k in keys:
            if k not in "json_metadata":
                if isinstance(block[k], dict) and isinstance(json_content[k], list):
                    self.assertEqual(list(block[k].values()), json_content[k])
                else:
                    self.assertEqual(block[k], json_content[k])
