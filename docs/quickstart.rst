Quickstart
==========

Crea
-----
The crea object is the connection to the Crea blockchain.
By creating this object different options can be set.

.. note:: All init methods of crea classes can be given
          the ``crea_instance=`` parameter to assure that
          all objects use the same crea object. When the
          ``crea_instance=`` parameter is not used, the
          crea object is taken from get_shared_crea_instance().

          :func:`crea.instance.shared_crea_instance` returns a global instance of crea.
          It can be set by :func:`crea.instance.set_shared_crea_instance` otherwise it is created
          on the first call.

.. code-block:: python

   from crea import Crea
   from crea.account import Account
   stm = Crea()
   account = Account("test", crea_instance=stm)

.. code-block:: python

   from crea import Crea
   from crea.account import Account
   from crea.instance import set_shared_crea_instance
   stm = Crea()
   set_shared_crea_instance(stm)
   account = Account("test")

Wallet and Keys
---------------
Each account has the following keys:

* Posting key (allows accounts to post, vote, edit, recrea and follow/mute)
* Active key (allows accounts to transfer, power up/down, voting for witness, ...)
* Memo key (Can be used to encrypt/decrypt memos)
* Owner key (The most important key, should not be used with crea)

Outgoing operation, which will be stored in the crea blockchain, have to be
signed by a private key. E.g. Comment or Vote operation need to be signed by the posting key
of the author or upvoter. Private keys can be provided to crea temporary or can be
stored encrypted in a sql-database (wallet).

.. note:: Before using the wallet the first time, it has to be created and a password has
          to set. The wallet content is available to creapy and all python scripts, which have
          access to the sql database file.

Creating a wallet
~~~~~~~~~~~~~~~~~
``crea.wallet.wipe(True)`` is only necessary when there was already an wallet created.

.. code-block:: python

   from crea import Crea
   crea = Crea()
   crea.wallet.wipe(True)
   crea.wallet.unlock("wallet-passphrase")

Adding keys to the wallet
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   from crea import Crea
   crea = Crea()
   crea.wallet.unlock("wallet-passphrase")
   crea.wallet.addPrivateKey("xxxxxxx")
   crea.wallet.addPrivateKey("xxxxxxx")

Using the keys in the wallet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from crea import Crea
   crea = Crea()
   crea.wallet.unlock("wallet-passphrase")
   account = Account("test", crea_instance=crea)
   account.transfer("<to>", "<amount>", "<asset>", "<memo>")

Private keys can also set temporary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from crea import Crea
   crea = Crea(keys=["xxxxxxxxx"])
   account = Account("test", crea_instance=crea)
   account.transfer("<to>", "<amount>", "<asset>", "<memo>")

Receiving information about blocks, accounts, votes, comments, market and witness
---------------------------------------------------------------------------------

Receive all Blocks from the Blockchain

.. code-block:: python

   from crea.blockchain import Blockchain
   blockchain = Blockchain()
   for op in blockchain.stream():
       print(op)

Access one Block

.. code-block:: python

   from crea.block import Block
   print(Block(1))

Access an account

.. code-block:: python

   from crea.account import Account
   account = Account("test")
   print(account.balances)
   for h in account.history():
       print(h)

A single vote

.. code-block:: python

   from crea.vote import Vote
   vote = Vote(u"@gtg/ffdhu-gtg-witness-log|gandalf")
   print(vote.json())

All votes from an account

.. code-block:: python

   from crea.vote import AccountVotes
   allVotes = AccountVotes("gtg")

Access a post

.. code-block:: python

   from crea.comment import Comment
   comment = Comment("@gtg/ffdhu-gtg-witness-log")
   print(comment["active_votes"])

Access the market

.. code-block:: python

   from crea.market import Market
   market = Market("CBD:CREA")
   print(market.ticker())

Access a witness

.. code-block:: python

   from crea.witness import Witness
   witness = Witness("gtg")
   print(witness.is_active)

Sending transaction to the blockchain
-------------------------------------

Sending a Transfer

.. code-block:: python

   from crea import Crea
   crea = Crea()
   crea.wallet.unlock("wallet-passphrase")
   account = Account("test", crea_instance=crea)
   account.transfer("null", 1, "CBD", "test")

Upvote a post

.. code-block:: python

   from crea.comment import Comment
   from crea import Crea
   crea = Crea()
   crea.wallet.unlock("wallet-passphrase")
   comment = Comment("@gtg/ffdhu-gtg-witness-log", crea_instance=crea)
   comment.upvote(weight=10, voter="test")

Publish a post to the blockchain

.. code-block:: python

   from crea import Crea
   crea = Crea()
   crea.wallet.unlock("wallet-passphrase")
   crea.post("title", "body", author="test", tags=["a", "b", "c", "d", "e"], self_vote=True)

Sell CREA on the market

.. code-block:: python

   from crea.market import Market
   from crea import Crea
   crea.wallet.unlock("wallet-passphrase")
   market = Market("CBD:CREA", crea_instance=crea)
   print(market.ticker())
   market.crea.wallet.unlock("wallet-passphrase")
   print(market.sell(300, 100))  # sell 100 CREA for 300 CREA/CBD
