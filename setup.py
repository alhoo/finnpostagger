#!/usr/bin/env python

from os import path
from codecs import open
from setuptools import find_packages, setup, Extension

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'finnpostagger',
  version = '0.0.1',
  description = 'Wrapper for the FinnPos tagger',
  long_description=long_description,
  author = 'Lasse Hyyrynen',
  author_email = 'leh@protonmail.com',
  maintainer = 'Lasse Hyyrynen',
  maintainer_email = 'leh@protonmail.com',
  license = 'MIT',
  keywords = ['nlp', 'pos', 'finnpos'],
  download_url = 'https://github.com/alhoo/finnpostagger/archive/0.5.1.tar.gz',
  url = 'https://github.com/alhoo/finnpostagger',
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Topic :: Utilities'
  ],
  packages = ['finnpostagger'],
  setup_requires = [
    'setuptools>=20.2.2'
  ],
  install_requires = [
    'regex>=2016.3.2',
    'PyYAML>=3.12',
    'nltk>=3.0',
  ],
  zip_safe = True
)

