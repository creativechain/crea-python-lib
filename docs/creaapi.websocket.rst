creaapi\.websocket
==================

This class allows subscribe to push notifications from the Crea
node.

.. code-block:: python

    from pprint import pprint
    from creaapi.websocket import CreaWebsocket

    ws = CreaWebsocket(
        "wss://gtg.crea.house:8090",
        accounts=["test"],
        on_block=print,
    )

    ws.run_forever()


.. autoclass:: creaapi.websocket.CreaWebsocket
    :members:
    :undoc-members:
    :private-members:
    :special-members:


