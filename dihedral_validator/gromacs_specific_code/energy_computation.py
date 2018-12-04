#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
import tempfile
import re

EXTRACT_OUTPUT_RE = '-+\n{} +([-+]?\d+.\d)'


def compute_free_energy(e_pot_liq: float, e_pot_gas: float, temperature: float, num_of_particles: float,
                        R_CONST: float = 0.0083144598):
    return e_pot_liq/num_of_particles - e_pot_gas + R_CONST*temperature # result in kJ/mol

def extract_from_edr_file(edr_file_path: str, choice: int, choice_string: str, g_energy_command: str = 'gmx energy'):
    # validate user input
    validate_path(edr_file_path)
    validate_number(choice)
    truncated_edr_file_path = edr_file_path.replace('.edr', '')
    with tempfile.NamedTemporaryFile() as outfile:
        p = subprocess.Popen('{} -f {} -o {}'.format(g_energy_command, truncated_edr_file_path, outfile.name),
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                             encoding='ascii')
        out, err = p.communicate('{:d}/n/n'.format(choice))
        # TODO check whether energy is also in out for gromacs4
        return extract_values_from_genergy_output(out, choice_string)


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


def extract_values_from_genergy_output(genergy_output: str, what_to_extract: str,
                                       re_to_capture_output: str = EXTRACT_OUTPUT_RE) -> float:
    '''
    Extracts interesting parts of string similar to:
    """Energy                      Average   Err.Est.       RMSD  Tot-Drift
    -------------------------------------------------------------------------------
    Potential                  -154.457       0.43    16.2399   0.167619  (kJ/mol)"""
    :param genergy_output:
    :return:
    '''
    formatted_re = re_to_capture_output.format(what_to_extract)
    return float(re.search(formatted_re, genergy_output).group(1))


if __name__ == '__main__':
    # validate_path('kupsko')
    # validate_number('16')
    # print(extract_from_edr_file('example/gromacs_specific_files/md-gas.edr', 9, 'Potential'))
    # print(extract_from_edr_file('example/gromacs_specific_files/md-liquid_10nsRB_bestHC.edr', 20, 'Density'))
    gas_potential = extract_from_edr_file('example/gromacs_specific_files/md-gas.edr', 9, 'Potential')
    liquid_potential = extract_from_edr_file('example/gromacs_specific_files/md-liquid_10nsRB_bestHC.edr', 10, 'Potential')
    print(compute_free_energy(liquid_potential, gas_potential, 280, 100))
