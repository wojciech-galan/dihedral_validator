#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys


def validate_arguments(arguments):
    if arguments.package == 'gromacs':
        pass
    else:
        raise RuntimeError('Unknown package {}'.format(arguments.package))

def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='')  # todo dodać opis
    parser.add_argument('infile', type=str, help='path to parameters file')
    parser.add_argument('package', type=str, help='package which will be used to validate parameters')
    parser.add_argument('--param_type', '-p', type=int, default=3, help='forcefield parameters type')
    group = parser.add_argument_group('gromacs', 'gromacs-specific arguments')
    # gromacs - specific
    group.add_argument('--itp_template', '-i', type=str, help='path to the template .itp file')
    group.add_argument('--gro_file', '-g', type=str, help='path to the .gro file')
    group.add_argument('--mdp_file', '-m', type=str, help='path to the .mdp file')
    group.add_argument('--top_file', '-t', type=str, help='path to the .top file')
    parsed_args = parser.parse_args(args)
    print(parsed_args)
    validate_arguments(parsed_args)


if __name__ == '__main__':
    main(sys.argv[1:])