#! /usr/bin/python
# -*- coding: utf-8 -*-

from typing import Dict
from dihedral_validator.gromacs_specific_code.create_top import create_top_file
from dihedral_validator.gromacs_specific_code.process_itp import prepare_itp_file


def prepare_files(itp_template_path: str, itp_out_path: str, new_params: Dict, params_type: int,
                  ipt_comment_substitution: Dict[str, str], ipt_general_comments: str, top_path: str,
                  molecules: Dict[str:int], system_line: str, forcefield_itp_path: str = 'oplsaa.ff/forcefield.itp',
                  newline: str = '\n'):
    prepare_itp_file(itp_template_path, new_params, params_type, itp_out_path, ipt_comment_substitution, ipt_general_comments, newline)
    create_top_file(itp_out_path, molecules, system_line, top_path, forcefield_itp_path, newline)
