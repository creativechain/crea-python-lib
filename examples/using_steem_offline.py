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
from crea.witness import Witness
from creabase import operations
from crea.transactionbuilder import TransactionBuilder
from creagraphenebase.account import PasswordKey, PrivateKey, PublicKey
from crea.crea import Crea
from crea.utils import parse_time, formatTimedelta
from creaapi.exceptions import NumRetriesReached
from crea.nodelist import NodeList
from creabase.transactions import getBlockParams
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# example wif
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


if __name__ == "__main__":
    stm_online = Crea()
    ref_block_num, ref_block_prefix = getBlockParams(stm_online)
    print("ref_block_num %d - ref_block_prefix %d" % (ref_block_num, ref_block_prefix))

    stm = Crea(offline=True)

    op = operations.Transfer({'from': 'creabot',
                              'to': 'holger80',
                              'amount': "0.001 CBD",
                              'memo': ""})
    tb = TransactionBuilder(crea_instance=stm)

    tb.appendOps([op])
    tb.appendWif(wif)
    tb.constructTx(ref_block_num=ref_block_num, ref_block_prefix=ref_block_prefix)
    tx = tb.sign(reconstruct_tx=False)
    print(tx.json())
