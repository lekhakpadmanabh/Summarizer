#!/usr/bin/env python
import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='KeyptSummarizer',
      version='1.0',
      description='Extracts key points from news articles',
      url='https://github.com/lekhakpadmanabh/Summarizer',
      long_description=read('README.md'),
      author='Pamdanabh',
      license='Apache',
      packages=['smrzr'],
     )
