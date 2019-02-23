from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import int, str
import sys
from datetime import timedelta
import time
import io
from crea.crea import Crea
import logging
from prettytable import PrettyTable
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    stm = Crea(node="https://nodes.creary.net")
    # stm = Crea(node="https://testnet.creaitdev.com")
    # stm = Crea(node="wss://appbasetest.timcliff.com")
    # stm = Crea(node="https://api.creaitstage.com")
    # stm = Crea(node="https://api.creaitdev.com")
    all_calls = stm.rpc.get_methods(api="jsonrpc")
    t = PrettyTable(["method", "args", "ret"])
    t.align = "l"
    t_condenser = PrettyTable(["method", "args", "ret"])
    t_condenser.align = "l"
    for call in all_calls:
        if "condenser" not in call:
            ret = stm.rpc.get_signature({'method': call}, api="jsonrpc")
            t.add_row([
                call,
                ret['args'],
                ret['ret']
            ])
        else:
            ret = stm.rpc.get_signature({'method': call}, api="jsonrpc")
            t_condenser.add_row([
                call,
                ret['args'],
                ret['ret']
            ])
    print("Finished. Write results...")
    with open('print_appbase.txt', 'w') as w:
        w.write(str(t))
    with open('print_appbase.html', 'w') as w:
        w.write(str(t.get_html_string()))
    with open('print_appbase_condenser.txt', 'w') as w:
        w.write(str(t_condenser))
    with open('print_appbase_condenser.html', 'w') as w:
        w.write(str(t_condenser.get_html_string()))
