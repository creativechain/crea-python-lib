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


if __name__ == "__main__":
    # stm = Crea(node="https://testnet.timcliff.com/")
    # stm = Crea(node="https://testnet.creaitdev.com")
    stm = Crea(node="https://nodes.creary.net")
    stm.wallet.unlock(pwd="pwd123")

    account = Account("creabot", crea_instance=stm)
    print(account.get_voting_power())

    account.transfer("holger80", 0.001, "CBD", "test")
