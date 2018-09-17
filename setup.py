#!/usr/bin/env python

import codecs

from setuptools import setup
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '0.1.2'

setup(
    name='crea-lib',
    version=VERSION,
    description='Python library for Crea',
    long_description=open('README.md').read(),
    download_url='https://github.com/creativechain/crea-python-lib/tarball/' + VERSION,
    author='Creativechain Foundation',
    author_email='info@creativechain.org',
    maintainer='Creativechain Foundation',
    maintainer_email='info@creativechain.org',
    url='http://library.creas.io/crea-python-lib',
    keywords=['crea', 'library', 'api', 'rpc', 'transactions'],
    packages=["creapy", "creapyapi", "creapybase"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial',
    ],
    install_requires=[
        "crea-graphenelib>=0.1.1",
        "websockets>=2.0",
        "scrypt>=0.7.1",
        "diff-match-patch>=20121119",
        "appdirs>=1.4.0",
        "python-frontmatter>=0.2.1",
        "pycrypto>=2.6.1",
        "funcy",
        "python-dateutil>=2.6.1",
        # "python-dateutil",
        # "secp256k1==0.13.2"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
