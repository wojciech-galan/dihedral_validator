#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os

class Wrapper():
    def __init__(self):
        super().__init__()

    def run(self, command):
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)


if __name__ == '__main__':
    w = Wrapper()
    w.run('grompp -f example/gromacs_specific_files/gas_10ns.mdp -p example/gromacs_specific_files/gas_10ns-qqAWA_q1_new_t3t4.top -c example/gromacs_specific_files/md-gas_10ns-qqAWA_q1.gro -o temp/md-gas.tpr -maxwarn 11')
    print('\n\n\n\n\n-----------------------------w---------------------\n\n\n')
    w.run('mdrun -deffnm temp/md-gas')