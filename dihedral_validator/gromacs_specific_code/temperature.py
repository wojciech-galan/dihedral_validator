#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
from typing import Pattern

TEMPERATURE_RE = re.compile('^ref_t\s+= +(\d+\.\d+)', re.MULTILINE)


def extract_temperature_in_K_from_mdp_file(path: str, temperature_re: Pattern = TEMPERATURE_RE) -> float:
    with open(path, 'r') as f:
        content = f.read()
        return float(temperature_re.search(content).group(1))


if __name__ == '__main__':
    # ref_t			= 298.15 ; 25*C
    print(extract_temperature_in_K_from_mdp_file('example/gromacs_specific_files/gas_10ns.mdp'))
