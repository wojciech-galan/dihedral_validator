#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from typing import Dict


def create_top_file(particle_itp_path: str, molecules: Dict[str, int], system_line: str, out_path: str,
                    forcefield_itp_path: str = 'oplsaa.ff/forcefield.itp', newline: str = '\n'):
    with open(out_path, 'w') as f:
        f.write('#include "{}"{}'.format(forcefield_itp_path, newline))
        f.write('#include "{}"{}'.format(particle_itp_path, newline))
        f.write(newline)
        f.write('[ system ]{}'.format(newline))
        f.write('{}{}'.format(system_line, newline))
        f.write(newline)
        f.write('[ molecules ]{}'.format(newline))
        for k, v in molecules.items():
            f.write('{}   {}{}'.format(k, v, newline))


if __name__ == '__main__':
    create_top_file("triacetin_qqAWA_q1_new_t3t4.itp", {'triacetin': 100}, 'single triacetin molecule dHvap',
                    os.path.join('temp', 'out_top'))
