#!/usr/bin/env python
import os
from distutils.core import setup

def find(dir):
    package, subdir = os.path.split(dir)
    matches = []
    for root, dirnames, filenames in os.walk(dir):
        root = root[len(package)+1:]
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return matches

setup(
    name = 'autodidact',
    version = '0.1',
    url = 'https://github.com/JaapJoris/autodidact',
    license = 'AGPL',
    packages = ['autodidact', 'bps', 'cas', 'adminsortable'],
    package_data = {'bps': find('bps/static') + find('bps/templates')},
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    maintainer = 'Wessel Dankers',
    maintainer_email = 'wsl@fruit.je',
)
