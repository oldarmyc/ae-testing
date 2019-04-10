#!/usr/bin/env python

import setuptools
import sys

requirements = ['lxml', 'requests']
if sys.version_info[:2] < (2, 7):
    requirements.append('argparse')


test_requirements = ['mock', 'nose']
if sys.version_info[:2] < (2, 7):
    test_requirements.extend(['flake8 < 3', 'unittest2'])
else:
    test_requirements.append('flake8')


setuptools.setup(
    name='ae_stress',
    version='0.0.1',
    url='https://github.com/oldarmyc/ae5-stress',
    license='Apache License, Version 2.0',
    author='Dave Kludt',
    author_email='dkludt@anaconda.com',
    description='Stress test for AE5 installed system',
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    extras_require={
        'tests': test_requirements
    },
    entry_points={
        'console_scripts': [
            'ae-testing=stress_test.testing:main'
        ]
    },
    packages=['stress_test'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
