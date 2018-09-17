Account
~~~~~~~

Obtaining data of an account.

.. code-block:: python

   from creapy.account import Account
   account = Account("jared")
   print(account)
   print(account.reputation())
   print(account.balances)

.. autoclass:: creapy.account.Account
   :members:
