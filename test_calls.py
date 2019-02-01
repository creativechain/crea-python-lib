from datetime import datetime, timedelta
from crea import Crea
from pprint import pprint
import collections
import json
import time
import sys
import os

crea = Crea(node=['https://node1.creary.net'], custom_chains={
    "CREA": {
        'chain_assets': [
            {
                'asset': 'CREA', 'id': 0, 'precision': 3, 'symbol': 'CREA'
            },
            {
                'asset': 'VESTS', 'id': 1, 'precision': 6, 'symbol': 'VESTS'
            }
        ],
        'chain_id': '0000000000000000000000000000000000000000000000000000000000000000',
        'min_version': '0.0.0',
        'prefix': 'CREA'
    }
})

block = crea.rpc.get_following({'account': 'ander7agar', 'start': '', 'type': 'blog', 'limit': 100}, api='follow')
print(json.dumps(block, sort_keys=True))
