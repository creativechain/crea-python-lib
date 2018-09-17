import random

from creapy.instance import shared_crea_instance
from creapybase import transactions

from .storage import configStorage as config


class Dex(object):
    """ This class allows to access calls specific for the internal
        exchange of CREA.

        :param Crea crea_instance: Crea() instance to use when accesing a RPC

    """
    crea = None
    assets = ["CREA", "CBD"]

    def __init__(self, crea_instance=None):
        self.crea = crea_instance or shared_crea_instance()
        # ensure market_history is registered
        self.crea.rpc.apis = list(set(self.crea.rpc.apis + ["market_history"]))
        self.crea.rpc.register_apis()

    def _get_asset(self, symbol):
        """ Return the properties of the assets tradeable on the
            network.

            :param str symbol: Symbol to get the data for (i.e. CREA, CBD, VESTS)
        """
        if symbol == "CREA":
            return {"symbol": "CREA",
                    "precision": 3
                    }
        elif symbol == "CBD":
            return {"symbol": "CBD",
                    "precision": 3
                    }
        elif symbol == "VESTS":
            return {"symbol": "VESTS",
                    "precision": 6
                    }
        else:
            return None

    def _get_assets(self, quote):
        """ Given the `quote` asset, return base. If quote is CBD, then
            base is CREA and vice versa.
        """
        assets = self.assets.copy()
        assets.remove(quote)
        base = assets[0]
        return self._get_asset(quote), self._get_asset(base)

    def returnTicker(self):
        """ Returns the ticker for all markets.

            Output Parameters:

            * ``latest``: Price of the order last filled
            * ``lowest_ask``: Price of the lowest ask
            * ``highest_bid``: Price of the highest bid
            * ``cbd_volume``: Volume of CBD
            * ``crea_volume``: Volume of CREA
            * ``percent_change``: 24h change percentage (in %)

            .. note::

                Market is CREA:CBD and prices are CBD per CREA!

            Sample Output:

            .. code-block:: js

                 {'highest_bid': 0.30100226633322913,
                  'latest': 0.0,
                  'lowest_ask': 0.3249636958897082,
                  'percent_change': 0.0,
                  'cbd_volume': 108329611.0,
                  'crea_volume': 355094043.0}


        """
        ticker = {}
        t = self.crea.rpc.get_ticker(api="market_history")
        ticker = {'highest_bid': float(t['highest_bid']),
                  'latest': float(t["latest"]),
                  'lowest_ask': float(t["lowest_ask"]),
                  'percent_change': float(t["percent_change"]),
                  'cbd_volume': t["cbd_volume"],
                  'crea_volume': t["crea_volume"]}
        return ticker

    def return24Volume(self):
        """ Returns the 24-hour volume for all markets, plus totals for primary currencies.

            Sample output:

            .. code-block:: js

                {'cbd_volume': 108329.611, 'crea_volume': 355094.043}

        """
        v = self.crea.rpc.get_volume(api="market_history")
        return {'cbd_volume': v["cbd_volume"],
                'crea_volume': v["crea_volume"]}

    def returnOrderBook(self, limit=25):
        """ Returns the order book for the CBD/CREA markets in both orientations.

            :param int limit: Limit the amount of orders (default: 25)

            .. note::

                Market is CREA:CBD and prices are CBD per CREA!

            Sample output:

            .. code-block:: js

                {'asks': [{'price': 3.086436224481787,
                           'bbd': 318547,
                           'crea': 983175},
                          {'price': 3.086429621198315,
                           'bbd': 2814903,
                           'crea': 8688000}],
                 'bids': [{'price': 3.0864376216446257,
                           'bbd': 545133,
                           'crea': 1682519},
                          {'price': 3.086440512632327,
                           'bbd': 333902,
                           'crea': 1030568}]},
        """
        orders = self.crea.rpc.get_order_book(limit, api="market_history")
        r = {"asks": [], "bids": []}
        for side in ["bids", "asks"]:
            for o in orders[side]:
                r[side].append({
                    'price': float(o["price"]),
                    'bbd': o["bbd"] / 10 ** 3,
                    'crea': o["crea"] / 10 ** 3,
                })
        return r

    def returnBalances(self, account=None):
        """ Return CBD and CREA balance of the account

            :param str account: (optional) the source account for the transfer if not ``default_account``
        """
        return self.crea.get_balances(account)

    def returnOpenOrders(self, account=None):
        """ Return open Orders of the account

            :param str account: (optional) the source account for the transfer if not ``default_account``
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        orders = self.crea.rpc.get_open_orders(account, limit=1000)
        return orders

    def returnTradeHistory(self, time=1 * 60 * 60, limit=100):
        """ Returns the trade history for the internal market

            :param int hours: Show the last x seconds of trades (default 1h)
            :param int limit: amount of trades to show (<100) (default: 100)
        """
        assert limit <= 100, "'limit' has to be smaller than 100"
        return self.crea.rpc.get_trade_history(
            transactions.formatTimeFromNow(-time),
            transactions.formatTimeFromNow(),
            limit,
            api="market_history"
        )

    def returnMarketHistoryBuckets(self):
        return self.crea.rpc.get_market_history_buckets(api="market_history")

    def returnMarketHistory(
        self,
        bucket_seconds=60 * 5,
        start_age=1 * 60 * 60,
        stop_age=0,
    ):
        """ Return the market history (filled orders).

            :param int bucket_seconds: Bucket size in seconds (see `returnMarketHistoryBuckets()`)
            :param int start_age: Age (in seconds) of the start of the window (default: 1h/3600)
            :param int end_age: Age (in seconds) of the end of the window (default: now/0)

            Example:

            .. code-block:: js

                 {'close_cbd': 2493387,
                  'close_crea': 7743431,
                  'high_cbd': 1943872,
                  'high_crea': 5999610,
                  'id': '7.1.5252',
                  'low_cbd': 534928,
                  'low_crea': 1661266,
                  'open': '2016-07-08T11:25:00',
                  'open_cbd': 534928,
                  'open_crea': 1661266,
                  'cbd_volume': 9714435,
                  'seconds': 300,
                  'crea_volume': 30088443},
        """
        return self.crea.rpc.get_market_history(
            bucket_seconds,
            transactions.formatTimeFromNow(-start_age - stop_age),
            transactions.formatTimeFromNow(-stop_age),
            api="market_history"
        )

    def buy(self,
            amount,
            quote_symbol,
            rate,
            expiration=7 * 24 * 60 * 60,
            killfill=False,
            account=None,
            orderid=None):
        """ Places a buy order in a given market (buy ``quote``, sell
            ``base`` in market ``quote_base``). If successful, the
            method will return the order creating (signed) transaction.

            :param number amount: Amount of ``quote`` to buy
            :param str quote_symbol: CREA, or CBD
            :param float price: price denoted in ``base``/``quote``
            :param number expiration: (optional) expiration time of the order in seconds (defaults to 7 days)
            :param bool killfill: flag that indicates if the order shall be killed if it is not filled (defaults to False)
            :param str account: (optional) the source account for the transfer if not ``default_account``
            :param int orderid: (optional) a 32bit orderid for tracking of the created order (random by default)

            Prices/Rates are denoted in 'base', i.e. the CREA:CBD market
            is priced in CBD per CREA.
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        # We buy quote and pay with base
        quote, base = self._get_assets(quote=quote_symbol)
        op = transactions.Limit_order_create(**{
            "owner": account,
            "orderid": orderid or random.getrandbits(32),
            "amount_to_sell": '{:.{prec}f} {asset}'.format(
                amount * rate,
                prec=base["precision"],
                asset=base["symbol"]),
            "min_to_receive": '{:.{prec}f} {asset}'.format(
                amount,
                prec=quote["precision"],
                asset=quote["symbol"]),
            "fill_or_kill": killfill,
            "expiration": transactions.formatTimeFromNow(expiration)
        })
        return self.crea.finalizeOp(op, account, "active")

    def sell(self,
             amount,
             quote_symbol,
             rate,
             expiration=7 * 24 * 60 * 60,
             killfill=False,
             account=None,
             orderid=None):
        """ Places a sell order in a given market (sell ``quote``, buy
            ``base`` in market ``quote_base``). If successful, the
            method will return the order creating (signed) transaction.

            :param number amount: Amount of ``quote`` to sell
            :param str quote_symbol: CREA, or CBD
            :param float price: price denoted in ``base``/``quote``
            :param number expiration: (optional) expiration time of the order in seconds (defaults to 7 days)
            :param bool killfill: flag that indicates if the order shall be killed if it is not filled (defaults to False)
            :param str account: (optional) the source account for the transfer if not ``default_account``
            :param int orderid: (optional) a 32bit orderid for tracking of the created order (random by default)

            Prices/Rates are denoted in 'base', i.e. the CREA:CBD market
            is priced in CBD per CREA.
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        # We buy quote and pay with base
        quote, base = self._get_assets(quote=quote_symbol)
        op = transactions.Limit_order_create(**{
            "owner": account,
            "orderid": orderid or random.getrandbits(32),
            "amount_to_sell": '{:.{prec}f} {asset}'.format(
                amount,
                prec=quote["precision"],
                asset=quote["symbol"]),
            "min_to_receive": '{:.{prec}f} {asset}'.format(
                amount * rate,
                prec=base["precision"],
                asset=base["symbol"]),
            "fill_or_kill": killfill,
            "expiration": transactions.formatTimeFromNow(expiration)
        })
        return self.crea.finalizeOp(op, account, "active")

    def cancel(self, orderid, account=None):
        """ Cancels an order you have placed in a given market.

            :param int orderid: the 32bit orderid
            :param str account: (optional) the source account for the transfer if not ``default_account``
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        op = transactions.Limit_order_cancel(**{
            "owner": account,
            "orderid": orderid,
        })
        return self.crea.finalizeOp(op, account, "active")

    def get_lowest_ask(self):
        """ Return the lowest ask.

            .. note::

                Market is CREA:CBD and prices are CBD per CREA!

            Example:

            .. code-block:: js

                 {'price': '0.32399833185738391',
                   'bbd': 320863,
                   'crea': 990323}
        """
        orders = self.returnOrderBook(1)
        return orders["asks"][0]

    def get_higest_bid(self):
        """ Return the highest bid.

            .. note::

                Market is CREA:CBD and prices are CBD per CREA!

            Example:

            .. code-block:: js

                 {'price': '0.32399833185738391',
                  'bbd': 320863,
                  'crea': 990323}
        """
        orders = self.returnOrderBook(1)
        return orders["bids"][0]

    def transfer(self, *args, **kwargs):
        """ Dummy to redirect to crea.transfer()
        """
        return self.crea.transfer(*args, **kwargs)
