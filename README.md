# CreaLib (Python)

This library is unmaintained, do not build productive buisness with it!
Please not the disclaimer in the license file!


Python Library for Crea
========================

Python 3 library for Crea!

Installation
------------

Install with `pip3`:

    $ sudo apt-get install libffi-dev libssl-dev python-dev python3-pip
    $ pip3 install crea-lib

Manual installation:

    $ git clone https://github.com/creativechain/crea-python-lib/
    $ cd crea-python-lib
    $ python3 setup.py install --user

Upgrade
-------

    $ pip3 install crea --user --upgrade

Additional dependencies
-----------------------

`creaapi.creaasyncclient`:
 * `asyncio==3.4.3`
 * `pyyaml==3.11`

Documentation
-------------

Documentation is written with the help of sphinx and can be compile to
html with:

    cd docs
    make html
