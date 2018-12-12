#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="dihedral_validator",
    version='0.0.0',
    description='no description',
    url='https://github.com/wojciech-galan/dihedral_validator',
    author='Wojciech Gałan',
    license='GNU GPL v3.0',

    packages=find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
        'console_scripts': [
            'dihedral_validator = dihedral_validator.__main__:main'
        ]

    }
)
