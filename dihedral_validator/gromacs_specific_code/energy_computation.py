#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
import tempfile


def compute_potential(edr_file_path: str, choice: int = 9, g_energy_command: str = 'gmx energy'):
    # validate user input
    validate_path(edr_file_path)
    validate_number(choice)
    truncated_edr_file_path = edr_file_path.replace('.edr', '')
    with tempfile.NamedTemporaryFile() as outfile:
        p = subprocess.Popen('{} -f {} -o {}'.format(g_energy_command, truncated_edr_file_path, outfile.name), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='ascii')
        out, err = p.communicate('9/n/n')
        # TODO check whether energy is also in out for gromacs4
        return extract_energy_from_genergy_output(out)


def validate_path(path: str):
    '''
    Raises FileNotFoundError when path not exists
    :param path:
    :return:
    '''
    with open(path, 'r'):
        pass


def validate_number(number: int):
    '''
    Raises RuntimeErrorm when number is not int
    :param number:
    :return:
    '''
    if not isinstance(number, int):
        raise RuntimeError('Argument should be integer')


def extract_energy_from_genergy_output(genergy_output:str) -> float:
    '''
    Extracts interesting parts of string similar to:
    """Energy                      Average   Err.Est.       RMSD  Tot-Drift
    -------------------------------------------------------------------------------
    Potential                  -154.457       0.43    16.2399   0.167619  (kJ/mol)"""
    :param genergy_output:
    :return:
    '''
    pass


if __name__ == '__main__':
    # validate_path('kupsko')
    # validate_number('16')
    print(os.listdir('.'))
    compute_potential('example/gromacs_specific_files/md-gas.edr')
