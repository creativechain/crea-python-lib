from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from datetime import datetime, timedelta
import time
import io
import logging

from crea.blockchain import Blockchain
from crea.block import Block
from crea.account import Account
from crea.amount import Amount
from creagraphenebase.account import PasswordKey, PrivateKey, PublicKey
from crea.crea import Crea
from crea.utils import parse_time, formatTimedelta
from creaapi.exceptions import NumRetriesReached
from crea.nodelist import NodeList
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

password = "secretPassword"
username = "crea5"
useWallet = False
walletpassword = "123"

if __name__ == "__main__":
    testnet_node = "https://testnet.crea.vc"
    stm = Crea(node=testnet_node)
    prefix = stm.prefix
    # curl --data "username=username&password=secretPassword" https://testnet.crea.vc/create
    if useWallet:
        stm.wallet.wipe(True)
        stm.wallet.create(walletpassword)
        stm.wallet.unlock(walletpassword)
    active_key = PasswordKey(username, password, role="active", prefix=prefix)
    owner_key = PasswordKey(username, password, role="owner", prefix=prefix)
    posting_key = PasswordKey(username, password, role="posting", prefix=prefix)
    memo_key = PasswordKey(username, password, role="memo", prefix=prefix)
    active_pubkey = active_key.get_public_key()
    owner_pubkey = owner_key.get_public_key()
    posting_pubkey = posting_key.get_public_key()
    memo_pubkey = memo_key.get_public_key()
    active_privkey = active_key.get_private_key()
    posting_privkey = posting_key.get_private_key()
    owner_privkey = owner_key.get_private_key()
    memo_privkey = memo_key.get_private_key()
    if useWallet:
        stm.wallet.addPrivateKey(owner_privkey)
        stm.wallet.addPrivateKey(active_privkey)
        stm.wallet.addPrivateKey(memo_privkey)
        stm.wallet.addPrivateKey(posting_privkey)
    else:
        stm = Crea(node=testnet_node,
                    wif={'active': str(active_privkey),
                         'posting': str(posting_privkey),
                         'memo': str(memo_privkey)})
    account = Account(username, crea_instance=stm)
    if account["name"] == "crea":
        account.disallow("crea1", permission='posting')
        account.allow('crea1', weight=1, permission='posting', account=None)
        account.follow("crea1")
    elif account["name"] == "crea5":
        account.allow('crea4', weight=2, permission='active', account=None)
    if useWallet:
        stm.wallet.getAccountFromPrivateKey(str(active_privkey))

    # stm.create_account("crea1", creator=account, password=password1)

    account1 = Account("crea1", crea_instance=stm)
    b = Blockchain(crea_instance=stm)
    blocknum = b.get_current_block().identifier

    account.transfer("crea1", 1, "CBD", "test")
    b1 = Block(blocknum, crea_instance=stm)
