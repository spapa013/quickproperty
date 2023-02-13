#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'quickproperty', 'version.py')) as f:
    exec(f.read())

setup(
    name='quickproperty',
    version=__version__,
    description="An alternative to Python's property descriptor that is fast to implement.",
    author='Stelios Papadopoulos',
    author_email='stelios@spapa.us',
    packages=find_packages(exclude=[]),
)