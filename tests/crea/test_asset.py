from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
from parameterized import parameterized
from crea import Crea
from crea.asset import Asset
from crea.instance import set_shared_crea_instance
from crea.exceptions import AssetDoesNotExistsException
from crea.nodelist import NodeList


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.bts = Crea(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            num_retries=10
        )
        cls.creait = Crea(
            node="https://nodes.creary.net",
            nobroadcast=True,
            num_retries=10
        )
        set_shared_crea_instance(cls.bts)

    @parameterized.expand([
        ("normal"),
        ("creait"),
    ])
    def test_assert(self, node_param):
        if node_param == "normal":
            stm = self.bts
        else:
            stm = self.creait
        with self.assertRaises(AssetDoesNotExistsException):
            Asset("FOObarNonExisting", full=False, crea_instance=stm)

    @parameterized.expand([
        ("normal", "CBD", "CBD", 3, "@@000000013"),
        ("normal", "CREA", "CREA", 3, "@@000000021"),
        ("normal", "VESTS", "VESTS", 6, "@@000000037"),
        ("normal", "@@000000013", "CBD", 3, "@@000000013"),
        ("normal", "@@000000021", "CREA", 3, "@@000000021"),
        ("normal", "@@000000037", "VESTS", 6, "@@000000037"),
    ])
    def test_properties(self, node_param, data, symbol_str, precision, asset_str):
        if node_param == "normal":
            stm = self.bts
        else:
            stm = self.testnet
        asset = Asset(data, full=False, crea_instance=stm)
        self.assertEqual(asset.symbol, symbol_str)
        self.assertEqual(asset.precision, precision)
        self.assertEqual(asset.asset, asset_str)

    @parameterized.expand([
        ("normal"),
        ("creait"),
    ])
    def test_assert_equal(self, node_param):
        if node_param == "normal":
            stm = self.bts
        else:
            stm = self.creait
        asset1 = Asset("CBD", full=False, crea_instance=stm)
        asset2 = Asset("CBD", full=False, crea_instance=stm)
        self.assertTrue(asset1 == asset2)
        self.assertTrue(asset1 == "CBD")
        self.assertTrue(asset2 == "CBD")
        asset3 = Asset("CREA", full=False, crea_instance=stm)
        self.assertTrue(asset1 != asset3)
        self.assertTrue(asset3 != "CBD")
        self.assertTrue(asset1 != "CREA")

        a = {'asset': '@@000000021', 'precision': 3, 'id': 'CREA', 'symbol': 'CREA'}
        b = {'asset': '@@000000021', 'precision': 3, 'id': '@@000000021', 'symbol': 'CREA'}
        self.assertTrue(Asset(a, crea_instance=stm) == Asset(b, crea_instance=stm))

    """
    # Mocker comes from pytest-mock, providing an easy way to have patched objects
    # for the life of the test.
    def test_calls(mocker):
        asset = Asset("USD", lazy=True, crea_instance=Crea(offline=True))
        method = mocker.patch.object(Asset, 'get_call_orders')
        asset.calls
        method.assert_called_with(10)
    """
