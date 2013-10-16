#!/usr/bin/env python

from setuptools import setup, find_packages


PROJECT = 'overalls'
VERSION = '0.1'
AUTHOR = 'Simon Cross'
AUTHOR_EMAIL = 'hodgestar@gmail.com'
DESC = "Coveralls coverage uploader."

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    scripts=[
        'scripts/overalls',
    ],
    requires=[
        'requests',
    ],
    build_requires=[
        'pytest',
        'pytest-cov',
        'pytest-pep8',
        'mock',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
