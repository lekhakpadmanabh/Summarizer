#!/usr/bin/env python
import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(name='smrzr',
      version='0.1',
      description='Extracts key points from news articles',
      url='https://github.com/lekhakpadmanabh/Summarizer',
      long_description=open('README.md').read(),
      author='Pamdanabh',
      license='Apache',
      download_url='https://github.com/lekhakpadmanabh/Summarizer/tarball/0.1',
      packages=['smrzr'],
     )
