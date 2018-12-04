#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os

def validate_path(path:str):
    '''
    Raises FileNotFoundError when path not exists
    :param path:
    :return:
    '''
    with open(path, 'r'):
        pass

def validate_number(number:int):
    '''
    Raises RuntimeErrorm when number is not int
    :param number:
    :return:
    '''
    if not isinstance(number, int):
        raise RuntimeError('Argument should be integer')



if __name__ == '__main__':
    # validate_path('kupsko')
    # validate_number('16')
    compute_potential_gas()
