#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'test':
    os.system('./runtests.py')
    sys.exit()

setup(
    name = 'autodidact',
    version = '1.3',
    url = 'https://github.com/JaapJoris/autodidact',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    maintainer = 'Wessel Dankers',
    maintainer_email = 'wsl@fruit.je',
    license = 'AGPL',
    packages = find_packages(),
    zip_safe = False,
    include_package_data = True,
    install_requires = [
        'django >= 1.7.7, <= 1.9.4',
        'markdown >= 2.5.1, <= 2.6.5',
        'pillow >= 2.6.1, <= 3.1.1',
        'six >= 1.8.0, <= 1.10.0',
        'django-cleanup == 0.4.2',
        'django-pandocfield == 0.2.1',
        'django-orderedmodel == 0.1',
    ],
)
