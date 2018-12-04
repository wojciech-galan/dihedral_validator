#! /usr/bin/python
# -*- coding: utf-8 -*-

from typing import Dict
from dihedral_validator.gromacs_specific_code.create_top import create_top_file
from dihedral_validator.gromacs_specific_code.process_itp import prepare_itp_file


def prepare_files(itp_template_path: str, itp_out_path: str, new_params: Dict, params_type: int,
                  ipt_comment_substitution: Dict[str, str], top_path: str, molecules: Dict[str:int], system_line: str,
                  forcefield_itp_path: str = 'oplsaa.ff/forcefield.itp', newline: str = '\n'):
    pass
