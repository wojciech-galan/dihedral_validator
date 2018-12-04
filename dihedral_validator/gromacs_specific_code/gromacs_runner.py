#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
from dihedral_validator.command_wrapper import SimpleCommandWrapper

if __name__ == '__main__':
    w = SimpleCommandWrapper()
    w.run('grompp -f example/gromacs_specific_files/gas_10ns.mdp -p example/gromacs_specific_files/gas_10ns-qqAWA_q1_new_t3t4.top -c example/gromacs_specific_files/md-gas_10ns-qqAWA_q1.gro -o temp/md-gas.tpr -maxwarn 11')
    print('\n\n\n\n\n-----------------------------w---------------------\n\n\n')
    w.run('mdrun -deffnm temp/md-gas')