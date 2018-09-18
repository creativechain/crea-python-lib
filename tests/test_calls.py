from datetime import datetime, timedelta
from creapyapi.creanoderpc import CreaNodeRPC
from pprint import pprint
import collections
import json
import time
import sys
import os

rpc = CreaNodeRPC("http://54.36.218.80:8091", "", "", apis=["follow", "block", "database"])

block = rpc.get_blog(api="follow_api", account="ander7agar", start_entry_id=0, limit=500)
print(json.dumps(block, sort_keys=True))
