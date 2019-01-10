#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from dihedral_validator.input import read_input_file
from dihedral_validator.gromacs_specific_code.gromacs_pipeline import gromacs_pipeline

PERMITTED_VALUES = {
    'packages': ['gromacs'],
    'param_types': [3]
}


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='')  # todo dodać opis
    parser.add_argument('package', type=str, help='package which will be used to validate parameters')
    parser.add_argument('params_file', type=str, help='file containing parameters to be validated')
    parser.add_argument('--param_type', '-p', type=int, default=3, help='forcefield parameters type')
    # gromacs - specific
    group = parser.add_argument_group('gromacs', 'gromacs-specific arguments')
    group.add_argument('--itp_template', type=str, help='path to the template .itp file')
    group.add_argument('--itp_output', type=str, help='output .itp file path')
    group.add_argument('--gro_gas_file', '-g', type=str, help='path to the .gro file regarding gas phase')
    group.add_argument('--gro_liquid_file', type=str, help='path to the .gro file regarding liquid phase')
    group.add_argument('--mdp_gas_file', type=str, help='path to the .mdp file regarding gas phase')
    group.add_argument('--mdp_liquid_file', type=str, help='path to the .mdp file regarding liquid phase')
    group.add_argument('--top_gas_file', type=str, help='path to the .top file regarding gas phase')
    group.add_argument('--top_liquid_file', type=str, help='path to the .top file regarding liquid phase')
    group.add_argument('--molecules_liquid_num', type=int, help='number of molecules in liquid phase')
    group.add_argument('--molecules_type', type=str, help='type of molecules')
    group.add_argument('--molecules_gas_num', type=int, default=1, help='number of molecules in gas phase')
    group.add_argument('--system_string', type=str, default='single triacetin molecule dHvap',
                       help='system section in .top file')
    parsed_args = parser.parse_args(args)
    validate_arguments(parsed_args)
    print(run_analysis(parsed_args))


def run_analysis(arguments):
    if arguments.package == 'gromacs':
        return gromacs_pipeline(arguments.itp_template, arguments.itp_output, arguments.params_file,
                                arguments.param_type, {}, 'File generated with dihedral_validator',
                                arguments.top_liquid_file, arguments.mdp_liquid_file,
                                arguments.gro_liquid_file, arguments.top_gas_file, arguments.mdp_gas_file,
                                arguments.gro_gas_file, {arguments.molecules_type: arguments.molecules_liquid_num},
                                {arguments.molecules_type: arguments.molecules_gas_num}, arguments.system_string)


def validate_arguments(arguments, permited_values: dict = PERMITTED_VALUES):
    params = read_input_file(arguments.params_file)
    assert isinstance(params, dict)
    assert arguments.package in permited_values['packages']
    assert arguments.param_type in permited_values['param_types']
    if arguments.package == 'gromacs':
        for arg_name in ['itp_template', 'gro_gas_file', 'gro_liquid_file', 'mdp_gas_file', 'mdp_liquid_file']:
            try_open_for_reading(eval('arguments.{}'.format(arg_name)))
        for arg_name in ['itp_output', 'top_gas_file', 'top_liquid_file']:
            path = os.path.dirname(os.path.abspath(eval('arguments.{}'.format(arg_name))))
            check_directory_write_access(path)
    else:
        raise RuntimeError('Unknown package {}'.format(arguments.package))


def try_open_for_reading(path: str):
    with open(path, 'r') as _:
        pass


def check_directory_write_access(path: str):
    if not os.access(path, os.W_OK):
        raise OSError('Either {} directory does not exist or you cannot write to it.'.format(os.path.abspath(path)))


if __name__ == '__main__':
    main(sys.argv[1:])
