from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from crea import Crea
from crea.market import Market
from crea.price import Price
from crea.asset import Asset
from crea.amount import Amount
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
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_crea_instance(cls.bts)
        cls.bts.set_default_account("test")

    def test_market(self):
        bts = self.bts
        m1 = Market(u'CREA', u'CBD', crea_instance=bts)
        self.assertEqual(m1.get_string(), u'CBD:CREA')
        m2 = Market(crea_instance=bts)
        self.assertEqual(m2.get_string(), u'CBD:CREA')
        m3 = Market(u'CREA:CBD', crea_instance=bts)
        self.assertEqual(m3.get_string(), u'CREA:CBD')
        self.assertTrue(m1 == m2)

        base = Asset("CBD", crea_instance=bts)
        quote = Asset("CREA", crea_instance=bts)
        m = Market(base, quote, crea_instance=bts)
        self.assertEqual(m.get_string(), u'CREA:CBD')

    def test_ticker(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        ticker = m.ticker()
        self.assertEqual(len(ticker), 6)
        self.assertEqual(ticker['crea_volume']["symbol"], u'CREA')
        self.assertEqual(ticker['sbd_volume']["symbol"], u'CBD')

    def test_volume(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        volume = m.volume24h()
        self.assertEqual(volume['CREA']["symbol"], u'CREA')
        self.assertEqual(volume['CBD']["symbol"], u'CBD')

    def test_orderbook(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        orderbook = m.orderbook(limit=10)
        self.assertEqual(len(orderbook['asks_date']), 10)
        self.assertEqual(len(orderbook['asks']), 10)
        self.assertEqual(len(orderbook['bids_date']), 10)
        self.assertEqual(len(orderbook['bids']), 10)

    def test_recenttrades(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        recenttrades = m.recent_trades(limit=10)
        recenttrades_raw = m.recent_trades(limit=10, raw_data=True)
        self.assertEqual(len(recenttrades), 10)
        self.assertEqual(len(recenttrades_raw), 10)

    def test_trades(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        trades = m.trades(limit=10)
        trades_raw = m.trades(limit=10, raw_data=True)
        trades_history = m.trade_history(limit=10)
        self.assertEqual(len(trades), 10)
        self.assertTrue(len(trades_history) > 0)
        self.assertEqual(len(trades_raw), 10)

    def test_market_history(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        buckets = m.market_history_buckets()
        history = m.market_history(buckets[2])
        self.assertTrue(len(history) > 0)

    def test_accountopenorders(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        openOrder = m.accountopenorders("test")
        self.assertTrue(isinstance(openOrder, list))

    def test_buy(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        bts.txbuffer.clear()
        tx = m.buy(5, 0.1, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_create"
        )
        op = tx["operations"][0][1]
        self.assertIn("test", op["owner"])
        self.assertEqual(str(Amount('0.100 CREA', crea_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 CBD', crea_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"CBD:CREA", crea_instance=bts)
        tx = m.buy(p, 0.1, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.100 CREA', crea_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 CBD', crea_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"CBD:CREA", crea_instance=bts)
        a = Amount(0.1, "CREA", crea_instance=bts)
        tx = m.buy(p, a, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(a), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 CBD', crea_instance=bts)), op["amount_to_sell"])

    def test_sell(self):
        bts = self.bts
        bts.txbuffer.clear()
        m = Market(u'CREA:CBD', crea_instance=bts)
        tx = m.sell(5, 0.1, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_create"
        )
        op = tx["operations"][0][1]
        self.assertIn("test", op["owner"])
        self.assertEqual(str(Amount('0.500 CBD', crea_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 CREA', crea_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"CBD:CREA")
        tx = m.sell(p, 0.1, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.500 CBD', crea_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 CREA', crea_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"CBD:CREA", crea_instance=bts)
        a = Amount(0.1, "CREA", crea_instance=bts)
        tx = m.sell(p, a, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.500 CBD', crea_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 CREA', crea_instance=bts)), op["amount_to_sell"])

    def test_cancel(self):
        bts = self.bts
        bts.txbuffer.clear()
        m = Market(u'CREA:CBD', crea_instance=bts)
        tx = m.cancel(5, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_cancel"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "test",
            op["owner"])

    def test_crea_usb_impied(self):
        bts = self.bts
        m = Market(u'CREA:CBD', crea_instance=bts)
        crea_usd = m.crea_usd_implied()
        self.assertGreater(crea_usd, 0)
