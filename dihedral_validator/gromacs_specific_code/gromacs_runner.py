#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
import re
from typing import Pattern

VERSION_RE = re.compile(':-\) .+ (\d+\.\d+(\.\d+)?) +\(-:')


def determine_version():
    # gmx -version works for gromasc 2018 and returns output to stdout
    p = subprocess.Popen('gmx -version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if out:
        return get_version_from_version_string(out.decode())
    else:
        # gmxcheck -v works for gromasc 4 and returns output to stderr
        p = subprocess.Popen('gmxcheck -v', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        version_string = out or err
        return get_version_from_version_string(version_string.decode())


def get_version_from_version_string(intro_string: str, version_re: Pattern = VERSION_RE):
    # example intro string fragments:
    # :-)  VERSION 4.6.5  (-:
    # :-) GROMACS - gmx energy, 2018.1 (-:
    return version_re.search(intro_string).group(1)


if __name__ == '__main__':
    print(get_version_from_version_string(':-)  VERSION 4.6.5  (-:'))
    print(get_version_from_version_string(' :-) GROMACS - gmx energy, 2018.1 (-:'))
    print(determine_version())
    # w = Wrapper()
    # w.run('grompp -f example/gromacs_specific_files/gas_10ns.mdp -p example/gromacs_specific_files/gas_10ns-qqAWA_q1_new_t3t4.top -c example/gromacs_specific_files/md-gas_10ns-qqAWA_q1.gro -o temp/md-gas.tpr -maxwarn 11')
    # print('\n\n\n\n\n-----------------------------w---------------------\n\n\n')
    # w.run('mdrun -deffnm temp/md-gas')
