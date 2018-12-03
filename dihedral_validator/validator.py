#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='')  # todo dodać opis
    parser.add_argument('infile', type=str, help='path to parameters file')
    parser.add_argument('--param_type', type=int, help='') # TODO pomoc
    # gromacs - specific

    parsed_args = parser.parse_args(args)

if __name__ == '__main__':
    main(sys.argv[1:])