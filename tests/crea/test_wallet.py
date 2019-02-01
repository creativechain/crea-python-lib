from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
import mock
from pprint import pprint
from crea import Crea, exceptions
from crea.account import Account
from crea.amount import Amount
from crea.asset import Asset
from crea.wallet import Wallet
from crea.instance import set_shared_crea_instance, shared_crea_instance
from crea.nodelist import NodeList

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

    def test_wallet_lock(self):
        stm = self.stm
        self.wallet.crea = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        self.assertTrue(self.wallet.unlocked())
        self.assertFalse(self.wallet.locked())
        self.wallet.lock()
        self.assertTrue(self.wallet.locked())

    def test_change_masterpassword(self):
        stm = self.stm
        self.wallet.crea = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        self.assertTrue(self.wallet.unlocked())
        self.wallet.changePassphrase("newPass")
        self.wallet.lock()
        self.assertTrue(self.wallet.locked())
        self.wallet.unlock(pwd="newPass")
        self.assertTrue(self.wallet.unlocked())
        self.wallet.changePassphrase("TestingOneTwoThree")
        self.wallet.lock()

    def test_Keys(self):
        stm = self.stm
        self.wallet.crea = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        keys = self.wallet.getPublicKeys()
        self.assertTrue(len(keys) > 0)
        pub = self.wallet.getPublicKeys()[0]
        private = self.wallet.getPrivateKeyForPublicKey(pub)
        self.assertEqual(private, wif)

    def test_account_by_pub(self):
        stm = self.stm
        self.wallet.crea = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        acc = Account("gtg")
        pub = acc["owner"]["key_auths"][0][0]
        acc_by_pub = self.wallet.getAccount(pub)
        self.assertEqual("gtg", acc_by_pub["name"])
        gen = self.wallet.getAccountsFromPublicKey(pub)
        acc_by_pub_list = []
        for a in gen:
            acc_by_pub_list.append(a)
        self.assertEqual("gtg", acc_by_pub_list[0])
        gen = self.wallet.getAllAccounts(pub)
        acc_by_pub_list = []
        for a in gen:
            acc_by_pub_list.append(a)
        self.assertEqual("gtg", acc_by_pub_list[0]["name"])
        self.assertEqual(pub, acc_by_pub_list[0]["pubkey"])

    def test_pub_lookup(self):
        stm = self.stm
        self.wallet.crea = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getOwnerKeyForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getMemoKeyForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getActiveKeyForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getPostingKeyForAccount("test")

    def test_pub_lookup_keys(self):
        stm = self.stm
        self.wallet.crea = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getOwnerKeysForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getActiveKeysForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getPostingKeysForAccount("test")

    def test_encrypt(self):
        stm = self.stm
        self.wallet.crea = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        self.wallet.masterpassword = "TestingOneTwoThree"
        self.assertEqual([self.wallet.encrypt_wif("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd"),
                          self.wallet.encrypt_wif("5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR")],
                         ["6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxThxsUW8epQi",
                          "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg"])
        self.wallet.masterpassword = "Satoshi"
        self.assertEqual([self.wallet.encrypt_wif("5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5")],
                         ["6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq"])
        self.wallet.masterpassword = "TestingOneTwoThree"

    def test_deencrypt(self):
        stm = self.stm
        self.wallet.crea = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        self.wallet.masterpassword = "TestingOneTwoThree"
        self.assertEqual([self.wallet.decrypt_wif("6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxThxsUW8epQi"),
                          self.wallet.decrypt_wif("6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg")],
                         ["5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd",
                          "5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR"])
        self.wallet.masterpassword = "Satoshi"
        self.assertEqual([self.wallet.decrypt_wif("6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq")],
                         ["5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5"])
        self.wallet.masterpassword = "TestingOneTwoThree"
