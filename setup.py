#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='KeyptSummarizer',
      version='1.0',
      description='Extracts key points from news articles',
      url='https://github.com/lekhakpadmanabh/Summarizer',
      long_description=read('README.md'),
      author='Pamdanabh',
      license='GPLv3',
      packages=['keyptsummarizer'],
     )
