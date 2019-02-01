from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from crea import Crea
from crea.instance import set_shared_crea_instance
from crea.amount import Amount
from crea.price import Price, Order, FilledOrder
from crea.asset import Asset
import unittest
from crea.nodelist import NodeList


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(crea_instance=Crea(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        crea = Crea(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_crea_instance(crea)

    def test_init(self):
        # self.assertEqual(1, 1)

        Price("0.315 CREA/CBD")
        Price(1.0, "CREA/CBD")
        Price(0.315, base="CREA", quote="CBD")
        Price(0.315, base=Asset("CREA"), quote=Asset("CBD"))
        Price({
            "base": {"amount": 1, "asset_id": "CBD"},
            "quote": {"amount": 10, "asset_id": "CREA"}})
        Price("", quote="10 CBD", base="1 CREA")
        Price("10 CBD", "1 CREA")
        Price(Amount("10 CBD"), Amount("1 CREA"))

    def test_multiplication(self):
        p1 = Price(10.0, "CREA/CBD")
        p2 = Price(5.0, "VESTS/CREA")
        p3 = p1 * p2
        p4 = p3.as_base("CBD")
        p4_2 = p3.as_quote("VESTS")

        self.assertEqual(p4["quote"]["symbol"], "VESTS")
        self.assertEqual(p4["base"]["symbol"], "CBD")
        # 10 CREA/CBD * 0.2 VESTS/CREA = 50 VESTS/CBD = 0.02 CBD/VESTS
        self.assertEqual(float(p4), 0.02)
        self.assertEqual(p4_2["quote"]["symbol"], "VESTS")
        self.assertEqual(p4_2["base"]["symbol"], "CBD")
        self.assertEqual(float(p4_2), 0.02)
        p3 = p1 * 5
        self.assertEqual(float(p3), 50)

        # Inline multiplication
        p5 = Price(10.0, "CREA/CBD")
        p5 *= p2
        p4 = p5.as_base("CBD")
        self.assertEqual(p4["quote"]["symbol"], "VESTS")
        self.assertEqual(p4["base"]["symbol"], "CBD")
        # 10 CREA/CBD * 0.2 VESTS/CREA = 2 VESTS/CBD = 0.02 CBD/VESTS
        self.assertEqual(float(p4), 0.02)
        p6 = Price(10.0, "CREA/CBD")
        p6 *= 5
        self.assertEqual(float(p6), 50)

    def test_div(self):
        p1 = Price(10.0, "CREA/CBD")
        p2 = Price(5.0, "CREA/VESTS")

        # 10 CREA/CBD / 5 CREA/VESTS = 2 VESTS/CBD
        p3 = p1 / p2
        p4 = p3.as_base("VESTS")
        self.assertEqual(p4["base"]["symbol"], "VESTS")
        self.assertEqual(p4["quote"]["symbol"], "CBD")
        # 10 CREA/CBD * 0.2 VESTS/CREA = 2 VESTS/CBD = 0.5 CBD/VESTS
        self.assertEqual(float(p4), 2)

    def test_div2(self):
        p1 = Price(10.0, "CREA/CBD")
        p2 = Price(5.0, "CREA/CBD")

        # 10 CREA/CBD / 5 CREA/VESTS = 2 VESTS/CBD
        p3 = p1 / p2
        self.assertTrue(isinstance(p3, (float, int)))
        self.assertEqual(float(p3), 2.0)
        p3 = p1 / 5
        self.assertEqual(float(p3), 2.0)
        p3 = p1 / Amount("1 CBD")
        self.assertEqual(float(p3), 0.1)
        p3 = p1
        p3 /= p2
        self.assertEqual(float(p3), 2.0)
        p3 = p1
        p3 /= 5
        self.assertEqual(float(p3), 2.0)

    def test_ltge(self):
        p1 = Price(10.0, "CREA/CBD")
        p2 = Price(5.0, "CREA/CBD")

        self.assertTrue(p1 > p2)
        self.assertTrue(p2 < p1)
        self.assertTrue(p1 > 5)
        self.assertTrue(p2 < 10)

    def test_leeq(self):
        p1 = Price(10.0, "CREA/CBD")
        p2 = Price(5.0, "CREA/CBD")

        self.assertTrue(p1 >= p2)
        self.assertTrue(p2 <= p1)
        self.assertTrue(p1 >= 5)
        self.assertTrue(p2 <= 10)

    def test_ne(self):
        p1 = Price(10.0, "CREA/CBD")
        p2 = Price(5.0, "CREA/CBD")

        self.assertTrue(p1 != p2)
        self.assertTrue(p1 == p1)
        self.assertTrue(p1 != 5)
        self.assertTrue(p1 == 10)

    def test_order(self):
        order = Order(Amount("2 CBD"), Amount("1 CREA"))
        self.assertTrue(repr(order) is not None)

    def test_filled_order(self):
        order = {"date": "1900-01-01T00:00:00", "current_pays": "2 CBD", "open_pays": "1 CREA"}
        filledOrder = FilledOrder(order)
        self.assertTrue(repr(filledOrder) is not None)
        self.assertEqual(filledOrder.json()["current_pays"], Amount("2.000 CBD").json())