from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from crea import Crea
from crea.instance import set_shared_crea_instance
from crea.transactionbuilder import TransactionBuilder
from creabase.signedtransactions import Signed_Transaction
from creabase.operations import Transfer
from crea.account import Account
from crea.block import Block
from creagraphenebase.base58 import Base58
from crea.amount import Amount
from crea.exceptions import (
    InsufficientAuthorityError,
    MissingKeyError,
    InvalidWifError,
    WalletLocked
)
from creaapi import exceptions
from crea.wallet import Wallet
from crea.utils import formatTimeFromNow
from crea.nodelist import NodeList
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        node_list = nodelist.get_nodes(exclude_limited=True)
        cls.stm = Crea(
            node=node_list,
            keys={"active": wif, "owner": wif, "memo": wif},
            nobroadcast=True,
            num_retries=10
        )
        cls.creait = Crea(
            node="https://nodes.creary.net",
            nobroadcast=True,
            keys={"active": wif, "owner": wif, "memo": wif},
            num_retries=10
        )
        set_shared_crea_instance(cls.stm)
        cls.stm.set_default_account("test")

    def test_emptyTransaction(self):
        stm = self.stm
        tx = TransactionBuilder(crea_instance=stm)
        self.assertTrue(tx.is_empty())
        self.assertTrue(tx["ref_block_num"] is not None)

    def test_verify_transaction(self):
        stm = self.stm
        block = Block(22005665, crea_instance=stm)
        trx = block.transactions[28]
        signed_tx = Signed_Transaction(trx)
        key = signed_tx.verify(chain=stm.chain_params, recover_parameter=False)
        public_key = format(Base58(key[0]), stm.prefix)
        self.assertEqual(public_key, "STM4tzr1wjmuov9ftXR6QNv7qDWsbShMBPQpuwatZsfSc5pKjRDfq")
