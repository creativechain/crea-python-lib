Transaction Builder
~~~~~~~~~~~~~~~~~~~

To build your own transactions and sign them

.. code-block:: python

   from creapy.transactionbuilder import TransactionBuilder
   from creapybase.operations import Vote
   tx = TransactionBuilder()
   tx.appendOps(Vote(
       **{"voter": voter,
          "author": post_author,
          "permlink": post_permlink,
          "weight": int(weight * CREA_1_PERCENT)}  # CREA_1_PERCENT = 100
   ))
   tx.appendSigner("jared", "posting")
   tx.sign()
   tx.broadcast()

.. autoclass:: creapy.transactionbuilder.TransactionBuilder
   :members:
