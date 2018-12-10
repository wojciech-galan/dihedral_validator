#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import tempfile
from typing import Dict
from dihedral_validator.gromacs_specific_code.create_top import create_top_file
from dihedral_validator.gromacs_specific_code.process_itp import prepare_itp_file
from dihedral_validator.input import read_input_file
from dihedral_validator.gromacs_specific_code.gromacs_runner import determine_version
from dihedral_validator.gromacs_specific_code.energy_computation import extract_from_edr_file
from dihedral_validator.gromacs_specific_code.energy_computation import compute_free_energy
from dihedral_validator.gromacs_specific_code.const import mdrun_dict, grompp_dict, genergy_dict
from dihedral_validator.command_wrapper import SimpleCommandWrapper


def gromacs_pipeline(itp_template_path: str, itp_out_path: str, new_params_path: str, params_type: int,
                     ipt_comment_substitution: Dict[str, str], ipt_general_comments: str, top_liquid_path: str,
                     mdp_liquid_path: str, gro_liquid_path: str, top_gas_path: str, mdp_gas_path: str, gro_gas_path: str,
                     molecules: Dict[str, int], system_line: str, forcefield_itp_path: str = 'oplsaa.ff/forcefield.itp',
                     newline: str = '\n'):
    itp_template_modification_time = time.asctime(time.gmtime(os.path.getmtime(itp_template_path)))
    params_modification_time = time.asctime(time.gmtime(os.path.getmtime(new_params_path)))
    itp_template_abspath = os.path.abspath(itp_template_path)
    params_abspath = os.path.abspath(new_params_path)
    time_now = time.asctime(time.gmtime())
    ipt_general_comments += '{}This file was created on {}{} based on template {} modified on {}{} and params {} modified on {}'.format(
        newline, time_now, newline, itp_template_abspath, itp_template_modification_time, newline, params_abspath,
        params_modification_time)
    new_params = read_input_file(new_params_path)
    gromacs_version = determine_version().split('.')[0]
    prepare_itp_file(itp_template_path, new_params, params_type, itp_out_path, ipt_comment_substitution,
                     ipt_general_comments, newline)
    create_top_file(os.path.abspath(itp_out_path), molecules, system_line, top_gas_path, forcefield_itp_path, newline) blah # todo do zmiany molekuły
    create_top_file(os.path.abspath(itp_out_path), molecules, system_line, top_liquid_path, forcefield_itp_path, newline)
    w = SimpleCommandWrapper()
    # gas
    with tempfile.NamedTemporaryFile() as tpr_file:
        grompp_cmd = '{} -f {} -p {} -c {} -o {} -maxwarn {}'.format(
            grompp_dict[gromacs_version], mdp_gas_path, top_gas_path, gro_path, tpr_file.name, len(new_params))
        print(grompp_cmd)
        # todo gdzie zrobić zrównoleglenie?
        # co z warningami?
        w.run(grompp_cmd)
        print(open(tpr_file.name, 'r').read())
        mdrun_cmd = '{} -deffnm {}'.format(mdrun_dict[gromacs_version], tpr_file.name)
        print(mdrun_cmd)
        w.run(mdrun_cmd)
        # to z dwóch różnych plików
        #liquid_potential = extract_from_edr_file(tpr_file.rsplit('.',1)[0], 10, 'Potential', gromacs_version)
        gas_potential = extract_from_edr_file(tpr_file.name.rsplit('.',1)[0], 9, 'Potential', gromacs_version)
        # num of particles from molecules variable?
    compute_free_energy(liquid_potential, gas_potential, temperature, num_of_particles)



if __name__ == '__main__':
    # grompp - f
    # example / gromacs_specific_files / gas_10ns.mdp - p
    # example / gromacs_specific_files / gas_10ns - qqAWA_q1_new_t3t4.top - c
    # example / gromacs_specific_files / md - gas_10ns - qqAWA_q1.gro - o
    # temp / md - gas.tpr
    gromacs_pipeline('example/gromacs_specific_files/triacetin_qqAWA_q1_new_t3t4.itp', 'temp/out_itp', 'example/input',
                     3, {}, '', 'temp/out_top.top',
                     'example/gromacs_specific_files/gas_10ns.mdp',
                     'example/gromacs_specific_files/md-gas_10ns-qqAWA_q1.gro', {'triacetin': 1},
                     'single triacetin molecule dHvap')  # TODO call the function with nonempty args
