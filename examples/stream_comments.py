from creaapi.creanoderpc import CreaNodeRPC
from pprint import pprint

rpc = CreaNodeRPC("wss://cread.creas.io/ws")

for a in rpc.stream("comment", start=1893850):
    pprint(a)
