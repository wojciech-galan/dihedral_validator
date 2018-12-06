#! /usr/bin/python
# -*- coding: utf-8 -*-

from typing import Dict
import os
import time
from dihedral_validator.gromacs_specific_code.create_top import create_top_file
from dihedral_validator.gromacs_specific_code.process_itp import prepare_itp_file
from dihedral_validator.input import read_input_file


def gromacs_pipeline(itp_template_path: str, itp_out_path: str, new_params_path: str, params_type: int,
                     ipt_comment_substitution: Dict[str, str], ipt_general_comments: str, top_path: str,
                     molecules: Dict[str:int], system_line: str, forcefield_itp_path: str = 'oplsaa.ff/forcefield.itp',
                     newline: str = '\n'):
    itp_template_modification_time = time.asctime(time.gmtime(os.path.getmtime(itp_template_path)))
    params_modification_time = time.asctime(time.gmtime(os.path.getmtime(new_params_path)))
    itp_template_abspath = os.path.abspath(itp_template_path)
    params_abspath = os.path.abspath(new_params_path)
    time_now = time.asctime(time.gmtime())
    ipt_general_comments += '{}This file was created on {}{} based on template {} modified on{}{} and params {} modified on {}'.format(
        newline, time_now, newline, itp_template_abspath, itp_template_modification_time, newline, params_abspath,
        params_modification_time)
    prepare_itp_file(itp_template_path, new_params, params_type, itp_out_path, ipt_comment_substitution,
                     ipt_general_comments, newline)
    create_top_file(itp_out_path, molecules, system_line, top_path, forcefield_itp_path, newline)
