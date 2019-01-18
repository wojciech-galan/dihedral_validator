#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import time
import copy
from dihedral_validator.input import read_input_file
from dihedral_validator.gromacs_specific_code.gromacs_pipeline import gromacs_pipeline
from dihedral_validator.lib import create_time_str_for_filename

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
    group.add_argument('--itp_output', type=str, help='output .itp file path', default=None)
    group.add_argument('--gro_gas_file', '-g', type=str, help='path to the .gro file regarding gas phase')
    group.add_argument('--gro_liquid_file', type=str, help='path to the .gro file regarding liquid phase')
    group.add_argument('--mdp_gas_file', type=str, help='path to the .mdp file regarding gas phase')
    group.add_argument('--mdp_liquid_file', type=str, help='path to the .mdp file regarding liquid phase')
    group.add_argument('--top_gas_file', type=str, help='path to the .top file regarding gas phase', default=None)
    group.add_argument('--top_liquid_file', type=str, help='path to the .top file regarding liquid phase', default=None)
    group.add_argument('--molecules_liquid_num', type=int, help='number of molecules in liquid phase')
    group.add_argument('--molecules_type', type=str, help='type of molecules')
    group.add_argument('--molecules_gas_num', type=int, default=1, help='number of molecules in gas phase')
    group.add_argument('--system_string', type=str, default='single triacetin molecule dHvap',
                       help='system section in .top file')
    group.add_argument('--out_dir', type=str, help='directory for output files', default=None)
    parsed_args = parser.parse_args(args)
    validate_arguments(parsed_args)
    out_dir_abspath = create_out_dir_path(parsed_args.out_dir)
    try:
        os.mkdir(out_dir_abspath)
    except FileExistsError as fee:
        raise FileExistsError('File {} already exists'.format(fee.filename))
    check_directory_write_access(out_dir_abspath)
    print(run_analysis(parsed_args, out_dir_abspath))


def run_analysis(arguments, out_dir_abspath:str):
    if arguments.package == 'gromacs':
        if arguments.itp_output:
            itp_out_path = os.path.abspath(arguments.itp_output)
        else:
            itp_template_filename = os.path.basename(arguments.itp_template)
            itp_out_path = os.path.join(out_dir_abspath, itp_template_filename)
        assert os.path.abspath(arguments.itp_template) != os.path.abspath(itp_out_path)
        if arguments.top_gas_file:
            top_gas_path = os.path.abspath(arguments.top_gas_file)
        else:
            top_gas_path = os.path.join(out_dir_abspath, 'gas.top')
        if arguments.top_liquid_file:
            top_liquid_path =os.path.abspath(arguments.top_liquid_file)
        else:
            top_liquid_path = os.path.join(out_dir_abspath, 'liquid.top')
        abs_itp_template = os.path.abspath(arguments.itp_template)
        abs_params_file = os.path.abspath(arguments.params_file)
        abs_mdp_liquid_file = os.path.abspath(arguments.mdp_liquid_file)
        abs_gro_liquid_file = os.path.abspath(arguments.gro_liquid_file)
        abs_mdp_gas_file = os.path.abspath(arguments.mdp_gas_file)
        abs_gro_gas_file = os.path.abspath(arguments.gro_gas_file)
        backup_dir = os.getcwd()
        os.chdir(out_dir_abspath)
        result = gromacs_pipeline(abs_itp_template, itp_out_path, abs_params_file,
                                arguments.param_type, {}, 'File generated with dihedral_validator',
                                top_liquid_path, abs_mdp_liquid_file,
                                abs_gro_liquid_file, top_gas_path, abs_mdp_gas_file,
                                abs_gro_gas_file, {arguments.molecules_type: arguments.molecules_liquid_num},
                                {arguments.molecules_type: arguments.molecules_gas_num}, arguments.system_string,
                                out_dir_abspath)
        os.chdir(backup_dir)
        return result


def validate_arguments(arguments, permited_values: dict = PERMITTED_VALUES):
    params = read_input_file(arguments.params_file)
    assert isinstance(params, dict)
    assert arguments.package in permited_values['packages']
    assert arguments.param_type in permited_values['param_types']
    if arguments.package == 'gromacs':
        for arg_name in ['gro_gas_file', 'gro_liquid_file', 'mdp_gas_file', 'mdp_liquid_file']:
            try_open_for_reading(eval('arguments.{}'.format(arg_name)))
        for arg_name in ['itp_output', 'top_gas_file', 'top_liquid_file']:
            argument = eval('arguments.{}'.format(arg_name))
            if argument:
                check_directory_write_access(os.path.abspath(argument))
    else:
        raise RuntimeError('Unknown package {}'.format(arguments.package))


def try_open_for_reading(path: str):
    with open(path, 'r') as _:
        pass


def check_directory_write_access(path: str):
    if not os.access(path, os.W_OK):
        raise OSError('Either {} directory does not exist or you cannot write to it.'.format(os.path.abspath(path)))


def create_out_dir_path(dir_name:str) -> str:
    if not dir_name:
        dir_name = 'out_' + create_time_str_for_filename(time.gmtime())
    return os.path.abspath(dir_name)


if __name__ == '__main__':
    main(sys.argv[1:])
