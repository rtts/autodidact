#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'autodidact',
    version = '0.1',
    url = 'https://github.com/JaapJoris/autodidact',
    license = 'AGPL',
    packages = ['autodidact', 'bps', 'cas', 'adminsortable'],
    package_data = {'bps': ['static/*', 'templates/*']},
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    maintainer = 'Wessel Dankers',
    maintainer_email = 'wsl@fruit.je',
)
