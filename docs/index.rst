.. python-crea documentation master file, created by
   sphinx-quickstart on Fri Jun  5 14:06:38 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. http://sphinx-doc.org/rest.html
   http://sphinx-doc.org/markup/index.html
   http://sphinx-doc.org/markup/para.html
   http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html
   http://rest-sphinx-memo.readthedocs.org/en/latest/ReST.html

.. image:: _static/crea-logo.svg
   :width: 300 px
   :alt: crea
   :align: center

Welcome to crea's documentation!
================================

Crea is a blockchain-based rewards platform for publishers to monetize
content and grow community.

It is based on *Graphene* (tm), a blockchain technology stack (i.e.
software) that allows for fast transactions and ascalable blockchain
solution. In case of Crea, it comes with decentralized publishing of
content.

The crea library has been designed to allow developers to easily
access its routines and make use of the network without dealing with all
the related blockchain technology and cryptography. This library can be
used to do anything that is allowed according to the Crea
blockchain protocol.


About this Library
------------------

The purpose of *crea* is to simplify development of products and
services that use the Crea blockchain. It comes with

* its own (bip32-encrypted) wallet
* RPC interface for the Blockchain backend
* JSON-based blockchain objects (accounts, blocks, prices, markets, etc)
* a simple to use yet powerful API
* transaction construction and signing
* push notification API
* *and more*

Quickstart
----------

.. note:: All methods that construct and sign a transaction can be given
          the ``account=`` parameter to identify the user that is going
          to affected by this transaction, e.g.:
          
          * the source account in a transfer
          * the accout that buys/sells an asset in the exchange
          * the account whos collateral will be modified

         **Important**, If no ``account`` is given, then the
         ``default_account`` according to the settings in ``config`` is
         used instead.

.. code-block:: python

   from crea import Crea
   crea = Crea()
   crea.wallet.unlock("wallet-passphrase")
   account = Account("test", crea_instance=crea)
   account.transfer("<to>", "<amount>", "<asset>", "<memo>")

.. code-block:: python

   from crea.blockchain import Blockchain
   blockchain = Blockchain()
   for op in blockchain.stream():
       print(op)

.. code-block:: python

   from crea.block import Block
   print(Block(1))

.. code-block:: python

   from crea.account import Account
   account = Account("test")
   print(account.balances)
   for h in account.history():
       print(h)

.. code-block:: python

   from crea.crea import Crea
   stm = Crea()
   stm.wallet.wipe(True)
   stm.wallet.create("wallet-passphrase")
   stm.wallet.unlock("wallet-passphrase")
   stm.wallet.addPrivateKey("512345678")
   stm.wallet.lock()

.. code-block:: python

   from crea.market import Market
   market = Market("CBD:CREA")
   print(market.ticker())
   market.crea.wallet.unlock("wallet-passphrase")
   print(market.sell(300, 100)  # sell 100 CREA for 300 CREA/CBD


General
-------
.. toctree::
   :maxdepth: 1

   installation
   quickstart
   tutorials
   cli
   configuration
   apidefinitions
   modules
   contribute
   support
   indices



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
