#!/usr/bin/env python

from setuptools import setup, find_packages


def parse_requirements(filename):
    """Parse a PIP requirements file."""
    with open(filename) as f:
        reqs = [line.strip() for line in f]
    reqs = [line for line in reqs if line]
    return reqs


PROJECT = 'overalls'
URL = 'https://github.com/hodgestar/overalls'
VERSION = '0.1'
AUTHOR = 'Simon Cross'
AUTHOR_EMAIL = 'hodgestar@gmail.com'
DESC = "Coveralls coverage uploader."

setup(
    name=PROJECT,
    url=URL,
    version=VERSION,
    description=DESC,
    long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    package_data={
        'overalls': [
            '*/tests/*.lcov',
        ],
    },
    scripts=[
        'scripts/overalls',
    ],
    requires=parse_requirements("requirements.pip"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
