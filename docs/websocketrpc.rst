************
CreaNodeRPC
************

.. warning:: This is a low level class that can be used in combination with
             ``CreaClient``. Do not use this class unless you know what
             you are doing!

This class allows to call API methods exposed by the witness node via
websockets.

Defintion
=========
.. autoclass:: creapyapi.creanoderpc.CreaNodeRPC
    :members: rpcexec, __getattr__
