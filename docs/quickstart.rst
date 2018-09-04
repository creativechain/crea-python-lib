Quickstart
##########

As a quickstart example, let's create a notification bot for our own account and have a daemon send out an email to us if someone referred to our user.

DPay Instance
~~~~~~~~~~~~~~

Let's start by creating an instance to the dPay network.

.. code-block:: python

    from dpaypy import DPay
    dpay = DPay()

.. note:: Per default, this call connects to the API node offered by dSite
          Inc. If their server is under heavy load, you may see better and
          faster results using your own server, passed as first argument.

Waiting for new comments
~~~~~~~~~~~~~~~~~~~~~~~~

Now we use `dpay.stream_comment()` to wait and inspect all new comments:

.. code-block:: python

   for comment in dpay.stream_comments():
       # do something with comment

The `comment` object is an instance of `DPay.Post` and offers the following calls:

* ``comment.reply()``
* ``comment.upvote()``
* ``comment.downvote()``

Most important attributes are probably:

* ``comment.author``
* ``comment.permlink``
* ``comment.title``
* ``comment.body``

These attributes can also be access through their keys (e.g. ``comment["body"]``).

For our notification, we simply check if `@accountname` exists in the body:

.. code-block:: python

   if "@%s" % accountname in c["body"]:
        # send mail

If this check evaluates as true, we send out an email.

Full Code
~~~~~~~~~

A full example for our notification daemon looks like this:

.. code-block:: python

    from dpaypy import DPay
    import os
    import sendgrid
    dpay = DPay()
    sg = sendgrid.SendGridClient(
        os.environ['SENDGRID_USERNAME'],
        os.environ['SENDGRID_PASSWORD']
    )
    message = sendgrid.Mail()
    addresses = {"jared": "mail@jrice.io"}
    # addresses = os.environ["ADDRESSES"]
    for c in dpay.stream_comments():
        for user in addresses.keys():
            if "@%s" % user in c["body"]:
                message.add_to(addresses[user])
                message.set_subject('Notification on dPay')
                message.set_text(
                    "You have been messaged by %s " % (c["author"]) +
                    "in the post @%s/%s" % (c["author"], c["permlink"]) +
                    "\n\n" +
                    "You can read the post on dSite.io:\n" +
                    "http://dsite.io/%s/%s#@%s/%s"
                    % (c["category"],
                        c["openingPostIdentifier"],
                        c["author"], c["permlink"])
                )
                message.set_from('notify@dpay')
                status, msg = sg.send(message)
                print("\nMessage sent!\n")
