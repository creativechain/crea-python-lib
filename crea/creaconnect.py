# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import json
try:
    from urllib.parse import urlparse, urlencode, urljoin
except ImportError:
    from urlparse import urlparse, urljoin
    from urllib import urlencode
import requests
from .storage import configStorage as config
from six import PY2
from crea.instance import shared_crea_instance
from crea.amount import Amount


class CreaConnect(object):
    """ CreaConnect

        :param str scope: comma separated string with scopes
            login,offline,vote,comment,delete_comment,comment_options,custom_json,claim_reward_balance


        .. code-block:: python

            # Run the login_app in examples and login with a account
            from crea import Crea
            from crea.creaconnect import CreaConnect
            from crea.comment import Comment
            sc2 = CreaConnect(client_id="crea.app")
            crea = Crea(creaconnect=sc2)
            crea.wallet.unlock("supersecret-passphrase")
            post = Comment("author/permlink", crea_instance=crea)
            post.upvote(voter="test")  # replace "test" with your account

        Examples for creating creaconnect v2 urls for broadcasting in browser:

        .. testoutput::

            from crea import Crea
            from crea.account import Account
            from crea.creaconnect import CreaConnect
            from pprint import pprint
            crea = Crea(nobroadcast=True, unsigned=True)
            sc2 = CreaConnect(crea_instance=crea)
            acc = Account("test", crea_instance=crea)
            pprint(sc2.url_from_tx(acc.transfer("test1", 1, "CREA", "test")))

        .. testcode::

            'https://creaconnect.com/sign/transfer?from=test&to=test1&amount=1.000+CREA&memo=test'

        .. testoutput::

            from crea import Crea
            from crea.transactionbuilder import TransactionBuilder
            from creabase import operations
            from crea.creaconnect import CreaConnect
            from pprint import pprint
            stm = Crea(nobroadcast=True, unsigned=True)
            sc2 = CreaConnect(crea_instance=stm)
            tx = TransactionBuilder(crea_instance=stm)
            op = operations.Transfer(**{"from": 'test',
                                        "to": 'test1',
                                        "amount": '1.000 CREA',
                                        "memo": 'test'})
            tx.appendOps(op)
            pprint(sc2.url_from_tx(tx.json()))

        .. testcode::

            'https://creaconnect.com/sign/transfer?from=test&to=test1&amount=1.000+CREA&memo=test'

    """

    def __init__(self, crea_instance=None, *args, **kwargs):
        self.crea = crea_instance or shared_crea_instance()
        self.access_token = None
        self.get_refresh_token = kwargs.get("get_refresh_token", False)
        self.hot_sign_redirect_uri = kwargs.get("hot_sign_redirect_uri", config["hot_sign_redirect_uri"])
        if self.hot_sign_redirect_uri == "":
            self.hot_sign_redirect_uri = None
        self.client_id = kwargs.get("client_id", config["sc2_client_id"])
        self.scope = kwargs.get("scope", "login")
        self.oauth_base_url = kwargs.get("oauth_base_url", config["oauth_base_url"])
        self.sc2_api_url = kwargs.get("sc2_api_url", config["sc2_api_url"])

    @property
    def headers(self):
        return {'Authorization': self.access_token}

    def get_login_url(self, redirect_uri, **kwargs):
        """ Returns a login url for receiving token from creaconnect
        """
        client_id = kwargs.get("client_id", self.client_id)
        scope = kwargs.get("scope", self.scope)
        get_refresh_token = kwargs.get("get_refresh_token", self.get_refresh_token)
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
        }
        if get_refresh_token:
            params.update({
                "response_type": "code",
            })
        if PY2:
            return urljoin(
                self.oauth_base_url,
                "authorize?" + urlencode(params).replace('%2C', ','))
        else:
            return urljoin(
                self.oauth_base_url,
                "authorize?" + urlencode(params, safe=","))

    def get_access_token(self, code):
        post_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.crea.wallet.getTokenForAccountName(self.client_id),
        }

        r = requests.post(
            urljoin(self.sc2_api_url, "oauth2/token/"),
            data=post_data
        )

        return r.json()

    def me(self, username=None):
        """ Calls the me function from creaconnect

        .. code-block:: python

            from crea.creaconnect import CreaConnect
            sc2 = CreaConnect()
            sc2.crea.wallet.unlock("supersecret-passphrase")
            sc2.me(username="test")

        """
        if username:
            self.set_username(username)
        url = urljoin(self.sc2_api_url, "me/")
        r = requests.post(url, headers=self.headers)
        return r.json()

    def set_access_token(self, access_token):
        """ Is needed for :func:`broadcast` and :func:`me`
        """
        self.access_token = access_token

    def set_username(self, username, permission="posting"):
        """ Set a username for the next :func:`broadcast` or :func:`me` operation.
            The necessary token is fetched from the wallet
        """
        if permission != "posting":
            self.access_token = None
            return
        self.access_token = self.crea.wallet.getTokenForAccountName(username)

    def broadcast(self, operations, username=None):
        """ Broadcast an operation

            Sample operations:

            .. code-block:: js

                [
                    [
                        'vote', {
                                    'voter': 'gandalf',
                                    'author': 'gtg',
                                    'permlink': 'crea-pressure-4-need-for-speed',
                                    'weight': 10000
                                }
                    ]
                ]

        """
        url = urljoin(self.sc2_api_url, "broadcast/")
        data = {
            "operations": operations,
        }
        if username:
            self.set_username(username)
        headers = self.headers.copy()
        headers.update({
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
        })

        r = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            return r.json()
        except ValueError:
            return r.content

    def refresh_access_token(self, code, scope):
        post_data = {
            "grant_type": "refresh_token",
            "refresh_token": code,
            "client_id": self.client_id,
            "client_secret": self.crea.wallet.getTokenForAccountName(self.client_id),
            "scope": scope,
        }

        r = requests.post(
            urljoin(self.sc2_api_url, "oauth2/token/"),
            data=post_data,
        )

        return r.json()

    def revoke_token(self, access_token):
        post_data = {
            "access_token": access_token,
        }

        r = requests.post(
            urljoin(self.sc2_api_url, "oauth2/token/revoke"),
            data=post_data
        )

        return r.json()

    def update_user_metadata(self, metadata):
        put_data = {
            "user_metadata": metadata,
        }
        r = requests.put(
            urljoin(self.sc2_api_url, "me/"),
            data=put_data, headers=self.headers)

        return r.json()

    def url_from_tx(self, tx, redirect_uri=None):
        """ Creates a link for broadcasting an operation

            :param dict tx: includes the operation, which should be broadcast
            :param str redirect_uri: Redirects to this uri, when set
        """
        if not isinstance(tx, dict):
            tx = tx.json()
        if "operations" not in tx or not tx["operations"]:
            return ''
        urls = []
        operations = tx["operations"]
        for op in operations:
            operation = op[0]
            params = op[1]
            for key in params:
                value = params[key]
                if isinstance(value, list) and len(value) == 3:
                    try:
                        amount = Amount(value, crea_instance=self.crea)
                        params[key] = str(amount)
                    except:
                        amount = None
                elif isinstance(value, bool):
                    if value:
                        params[key] = 1
                    else:
                        params[key] = 0
            urls.append(self.create_hot_sign_url(operation, params, redirect_uri=redirect_uri))
        if len(urls) == 1:
            return urls[0]
        else:
            return urls

    def create_hot_sign_url(self, operation, params, redirect_uri=None):
        """ Creates a link for broadcasting an operation

            :param str operation: operation name (e.g.: vote)
            :param dict params: operation dict params
            :param str redirect_uri: Redirects to this uri, when set
        """

        if not isinstance(operation, str) or not isinstance(params, dict):
            raise ValueError("Invalid Request.")

        base_url = self.sc2_api_url.replace("/api", "")
        if redirect_uri == "":
            redirect_uri = None

        if redirect_uri is None and self.hot_sign_redirect_uri is not None:
            redirect_uri = self.hot_sign_redirect_uri
        if redirect_uri is not None:
            params.update({"redirect_uri": redirect_uri})

        for key in params:
            if isinstance(params[key], list):
                params[key] = json.dumps(params[key])
        params = urlencode(params)
        url = urljoin(base_url, "sign/%s" % operation)
        url += "?" + params

        return url
