#!/usr/bin/env python
import os
from distutils.core import setup

def find_packages(exclude=[]):
    dirs = find_package_dirs(exclude)
    return [module_name(dir) for dir in dirs]

def find_package_data(exclude=[]):
    data = {}
    for dir in find_package_dirs(exclude):
        files = find_files(dir)
        if files:
            data[module_name(dir)] = files
    return data

def find_package_dirs(exclude=[]):
    packages = []
    for curdir, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude]
        if "__init__.py" in files and os.path.dirname(curdir) in packages + ['.']:
            packages.append(curdir)
    return packages

def find_files(dir):
    matches = []
    for curdir, dirs, files in os.walk(dir):
        for file in files:
            if not file.endswith(('.py', 'pyc', '.gitignore')):
                subdir = curdir.split(dir)[1].lstrip('/')
                matches.append(os.path.join(subdir, file))
    return matches

def module_name(dir):
    return dir.lstrip('/.').replace('/', '.')

setup(
    name = 'autodidact',
    version = '0.4',
    url = 'https://github.com/JaapJoris/autodidact',
    license = 'AGPL',
    packages = find_packages(exclude=['tests']),
    package_data = find_package_data(),
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    maintainer = 'Wessel Dankers',
    maintainer_email = 'wsl@fruit.je',
)
