from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes
from builtins import chr
from builtins import range
from builtins import super
import random
from pprint import pprint
from binascii import hexlify
from collections import OrderedDict

from creabase import (
    transactions,
    memo,
    operations,
    objects
)
from creabase.objects import Operation
from creabase.signedtransactions import Signed_Transaction
from creagraphenebase.account import PrivateKey
from creagraphenebase import account
from creabase.operationids import getOperationNameForId
from creagraphenebase.py23 import py23_bytes, bytes_types
from crea.amount import Amount
from crea.asset import Asset
from crea.crea import Crea
import time

from crea import Crea as creaCrea
from creabase.account import PrivateKey as creaPrivateKey
from creabase.transactions import SignedTransaction as creaSignedTransaction
from creabase import operations as creaOperations
from timeit import default_timer as timer


class BeemTest(object):

    def setup(self):
        self.prefix = u"CREA"
        self.default_prefix = u"STM"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"
        self.stm = Crea(offline=True)

    def doit(self, printWire=False, ops=None):
        ops = [Operation(ops)]
        tx = Signed_Transaction(ref_block_num=self.ref_block_num,
                                ref_block_prefix=self.ref_block_prefix,
                                expiration=self.expiration,
                                operations=ops)
        start = timer()
        tx = tx.sign([self.wif], chain=self.prefix)
        end1 = timer()
        tx.verify([PrivateKey(self.wif, prefix=u"STM").pubkey], self.prefix)
        end2 = timer()
        return end2 - end1, end1 - start


class CreaTest(object):

    def setup(self):
        self.prefix = u"CREA"
        self.default_prefix = u"STM"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"

    def doit(self, printWire=False, ops=None):
        ops = [creaOperations.Operation(ops)]
        tx = creaSignedTransaction(ref_block_num=self.ref_block_num,
                                    ref_block_prefix=self.ref_block_prefix,
                                    expiration=self.expiration,
                                    operations=ops)
        start = timer()
        tx = tx.sign([self.wif], chain=self.prefix)
        end1 = timer()
        tx.verify([creaPrivateKey(self.wif, prefix=u"STM").pubkey], self.prefix)
        end2 = timer()
        return end2 - end1, end1 - start


if __name__ == "__main__":
    crea_test = CreaTest()
    crea_test = BeemTest()
    crea_test.setup()
    crea_test.setup()
    crea_times = []
    crea_times = []
    loops = 50
    for i in range(0, loops):
        print(i)
        opCrea = creaOperations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": "111.110 CREA",
            "memo": "Fooo"
        })
        opBeem = operations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": Amount("111.110 CREA", crea_instance=Crea(offline=True)),
            "memo": "Fooo"
        })

        t_s, t_v = crea_test.doit(ops=opCrea)
        crea_times.append([t_s, t_v])

        t_s, t_v = crea_test.doit(ops=opBeem)
        crea_times.append([t_s, t_v])

    crea_dt = [0, 0]
    crea_dt = [0, 0]
    for i in range(0, loops):
        crea_dt[0] += crea_times[i][0]
        crea_dt[1] += crea_times[i][1]
        crea_dt[0] += crea_times[i][0]
        crea_dt[1] += crea_times[i][1]
    print("crea vs crea:\n")
    print("crea: sign: %.2f s, verification %.2f s" % (crea_dt[0] / loops, crea_dt[1] / loops))
    print("crea:  sign: %.2f s, verification %.2f s" % (crea_dt[0] / loops, crea_dt[1] / loops))
    print("------------------------------------")
    print("crea is %.2f %% (sign) and %.2f %% (verify) faster than crea" %
          (crea_dt[0] / crea_dt[0] * 100, crea_dt[1] / crea_dt[1] * 100))
