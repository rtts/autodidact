#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name = 'autodidact',
    version = '0.8rc1',
    url = 'https://github.com/JaapJoris/autodidact',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    maintainer = 'Wessel Dankers',
    maintainer_email = 'wsl@fruit.je',
    license = 'AGPL',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'django',
        'django-admin-sortable',
        'django-cleanup',
        'django-cas',
        'markdown',
    ],
)
