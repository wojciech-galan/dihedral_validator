#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import tempfile
import subprocess
from typing import Dict
from dihedral_validator.gromacs_specific_code.create_top import create_top_file
from dihedral_validator.gromacs_specific_code.process_itp import prepare_itp_file
from dihedral_validator.input import read_input_file
from dihedral_validator.gromacs_specific_code.gromacs_runner import determine_version
from dihedral_validator.gromacs_specific_code.energy_computation import extract_from_edr_file
from dihedral_validator.gromacs_specific_code.energy_computation import compute_free_energy
from dihedral_validator.gromacs_specific_code.const import mdrun_dict, grompp_dict, tpr_file_extension
from dihedral_validator.gromacs_specific_code.temperature import extract_temperature_in_K_from_mdp_file
from dihedral_validator.command_wrapper import SimpleCommandWrapper
from dihedral_validator.lib import create_time_str_for_filename


def gromacs_pipeline(itp_template_path: str, itp_out_path: str, new_params_path: str, params_type: int,
                     ipt_comment_substitution: Dict[str, str], ipt_general_comments: str, top_liquid_path: str,
                     mdp_liquid_path: str, gro_liquid_path: str, top_gas_path: str, mdp_gas_path: str,
                     gro_gas_path: str, molecules_liquid: Dict[str, int], molecules_gas: Dict[str, int],
                     system_line: str, gromacs_output_dir: str, forcefield_itp_path: str = 'oplsaa.ff/forcefield.itp',
                     newline: str = '\n'):
    itp_template_modification_time = time.asctime(time.gmtime(os.path.getmtime(itp_template_path)))
    params_modification_time = time.asctime(time.gmtime(os.path.getmtime(new_params_path)))
    itp_template_abspath = os.path.abspath(itp_template_path)
    params_abspath = os.path.abspath(new_params_path)
    time_simple_string = time.asctime(time.gmtime())
    ipt_general_comments += '{}This file was created on {}{} based on template {} modified on {}{} and params {} modified on {}'.format(
        newline, time_simple_string, newline, itp_template_abspath, itp_template_modification_time, newline,
        params_abspath,
        params_modification_time)
    new_params = read_input_file(new_params_path)
    gromacs_version = determine_version().split('.')[0]
    prepare_itp_file(itp_template_path, new_params, params_type, itp_out_path, ipt_comment_substitution,
                     ipt_general_comments, newline)
    create_top_file(os.path.abspath(itp_out_path), molecules_gas, system_line, top_gas_path, forcefield_itp_path,
                    newline)
    create_top_file(os.path.abspath(itp_out_path), molecules_liquid, system_line, top_liquid_path, forcefield_itp_path,
                    newline)
    command_wrapper = SimpleCommandWrapper()
    tpr_gas_file_name = os.path.join(os.path.abspath(gromacs_output_dir),
                                     create_time_str_for_filename(time.gmtime()) + '.tpr_gas')
    tpr_liquid_file_name = os.path.join(os.path.abspath(gromacs_output_dir),
                                        create_time_str_for_filename(time.gmtime()) + '.tpr_liquid')
    grompp_gas_cmd = '{} -f {} -p {} -c {} -o {} -maxwarn {}'.format(
        grompp_dict[gromacs_version], mdp_gas_path, top_gas_path, gro_gas_path, tpr_gas_file_name,
        len(new_params))
    grompp_liquid_cmd = '{} -f {} -p {} -c {} -o {} -maxwarn {}'.format(
        grompp_dict[gromacs_version], mdp_liquid_path, top_liquid_path, gro_liquid_path, tpr_liquid_file_name,
        len(new_params))
    print(grompp_gas_cmd)
    print(grompp_liquid_cmd)
    command_wrapper.run(grompp_gas_cmd)
    command_wrapper.run(grompp_liquid_cmd)
    edr_gas_file_name = '{}.edr'.format(tpr_gas_file_name)
    edr_liquid_file_name = '{}.edr'.format(tpr_liquid_file_name)
    # TODO co z warningami?
    mdrun_gas_cmd = prepare_mdrun_command(gromacs_version, tpr_gas_file_name, edr_gas_file_name)
    mdrun_liquid_cmd = prepare_mdrun_command(gromacs_version, tpr_liquid_file_name, edr_liquid_file_name)
    print(mdrun_gas_cmd)
    print(mdrun_liquid_cmd)
    command_wrapper.run(mdrun_gas_cmd)
    gas_potential = extract_from_edr_file(edr_gas_file_name, 9, 'Potential', gromacs_version)
    command_wrapper.run(mdrun_liquid_cmd)
    liquid_potential = extract_from_edr_file(edr_liquid_file_name, 10, 'Potential', gromacs_version)
    assert len(molecules_liquid) == 1
    temperature_gas = extract_temperature_in_K_from_mdp_file(mdp_gas_path)
    temperature_liquid = extract_temperature_in_K_from_mdp_file(mdp_liquid_path)
    assert temperature_gas == temperature_liquid
    return compute_free_energy(liquid_potential, gas_potential, temperature_gas, list(molecules_liquid.values())[0])


def run_subprocesses_simultaneously(cmd1, cmd2, **kwargs):
    p1 = subprocess.Popen(cmd1, **kwargs)
    p2 = subprocess.Popen(cmd2, **kwargs)
    p1.wait()
    p2.wait()


def prepare_mdrun_command(gromacs_version: str, tpr_filename: str, edr_filename: str = None):
    base_cmd = mdrun_dict[gromacs_version]
    tpr_final_filename = '{}{}'.format(tpr_filename, tpr_file_extension[gromacs_version])
    if gromacs_version == '2018':
        return '{} -s {} -e {}'.format(base_cmd, tpr_final_filename, edr_filename)
    elif gromacs_version == '4':
        return '{} -deffnm {}'.format(base_cmd, tpr_final_filename)
    else:
        raise RuntimeError('Gromacs version not supported')


if __name__ == '__main__':
    # grompp - f
    # example / gromacs_specific_files / gas_10ns.mdp - p
    # example / gromacs_specific_files / gas_10ns - qqAWA_q1_new_t3t4.top - c
    # example / gromacs_specific_files / md - gas_10ns - qqAWA_q1.gro - o
    # temp / md - gas.tpr
    print(gromacs_pipeline('example/gromacs_specific_files/triacetin_qqAWA_q1_new_t3t4.itp', 'temp/out_itp',
                           'example/input', 3, {}, '', 'temp/liquid_top.top',
                           'example/gromacs_specific_files/liquid_10ns.mdp',
                           'example/gromacs_specific_files/md-liquid_10ns-qqAWA_q1.gro',
                           'temp/gas_top.top', 'example/gromacs_specific_files/gas_10ns.mdp',
                           'example/gromacs_specific_files/md-gas_10ns-qqAWA_q1.gro', {'triacetin': 100},
                           {'triacetin': 1}, 'single triacetin molecule dHvap',
                           'blah'))  # TODO call the function with nonempty args
