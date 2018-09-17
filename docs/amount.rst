Amount
~~~~~~

For the sake of easier handling of Assets on the blockchain

.. code-block:: python

   from creapy.amount import Amount
   a = Amount("1 CBD")
   b = Amount("20 CBD")
   a + b
   a * 2
   a += b
   a /= 2.0

.. autoclass:: creapy.amount.Amount
   :members:
