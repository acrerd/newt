#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'numpy',
    'matplotlib'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='newt',
    description="Access to data at the University of Glasgow Acre Road Observatory.",
    long_description=readme + '\n\n' + history,
    author="Daniel Williams",
    author_email='daniel.williams@glasgow.ac.uk',
    url='https://github.com/acrerd/newt',
    packages=[
        'newt',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    package_dir={
        'otter': 'otter'
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords=['newt','acreroad','glasgow'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
