#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Routines to create .itp file from template"""

import os
import re
from typing import Dict
from typing import Pattern
from typing import Match
from typing import List

SECTION_RE_TEMPLATE = '^\[ {} \]$\n(^.+$\n)+'
DEFINE_RE = re.compile('^#define .+')
COMMENT_RE = re.compile('(^;.*\n)+', re.MULTILINE)


def prepare_itp_file(in_ipt: str, new_params: dict, params_type: int, out_itp: str,
                     comment_substitution: Dict[str, str]):
    defines, sections_dict = parse_itp_file(in_ipt)
    for k, v in sections_dict:
        if filter_out_comments.get(k, False):
            sections_dict[k] = remove_lines_containing_comments[v]

def substitute_comment(section_string:str, new_comment:str, comment_re:Pattern=COMMENT_RE, newline:str='\n') -> str:
    '''
    Substitutes comments in section_string with new_comment
    :param section_string:
    :param new_comment:
    :return:
    '''
    replacement_string = newline.join(['; ' + s for s in new_comment.split(newline)]) + newline
    return comment_re.sub(replacement_string, section_string)

def create_dihedraltypes(params, base_comment_string:str =';  i    j    k    l   func     coefficients', additional_comment_string=';', newline='\n'):
    s = newline.join(['[ dihedraltypes ]', base_comment_string, additional_comment_string]) + newline
    for k, v in params.items():
        v = v + [0 for i in range(6-len(v))]
        print(k, adapt_input_dihedral_types_to_gromacs_format(k))
        s+= '{} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f}{}'.format(adapt_input_dihedral_types_to_gromacs_format(k), *v, newline)
    return s


def adapt_input_dihedral_types_to_gromacs_format(input_dihedral:str) -> str:
    # example input: CT-CT-CT-OS
    # example output: CT    CT   CT   OS
    a, b, c, d = input_dihedral.split('-')
    return '{}    {}   {}   {}'.format(a, b, c, d)


def parse_itp_file(in_file: str, newline='\n', section_re_template: str = SECTION_RE_TEMPLATE,
                   define_re: str = DEFINE_RE):
    with open(in_file, 'r') as f:
        content = f.read()
    defines = re.findall(define_re, content)
    #dihedraltypes = find_section('dihedraltypes', content, section_re_template=section_re_template)
    moleculetype = find_section('moleculetype', content, section_re_template=section_re_template)
    atoms = find_section('atoms', content, section_re_template=section_re_template)
    bonds = find_section('bonds', content, section_re_template=section_re_template)
    angles = find_section('angles', content, section_re_template=section_re_template)
    dihedrals1_math = find_section('dihedrals', content, section_re_template=section_re_template, return_match=True)
    dihedrals1 = dihedrals1_math.group(0)
    pairs = find_section('pairs', content, section_re_template=section_re_template)
    dihedrals2 = find_section('dihedrals', content, section_re_template=section_re_template,
                              start_pos=dihedrals1_math.end())
    ret_dict = {}
    for element in ['moleculetype', 'atoms', 'bonds', 'angles', 'dihedrals1', 'dihedrals2', 'pairs']:
        ret_dict[element] = locals()[element]
    return defines, ret_dict


def remove_lines_containing_comments(itp_file_content: str, newline='\n') -> str:
    ret_lines = []
    for line in itp_file_content.split(newline):
        if not line.lstrip().startswith(';'):
            ret_lines.append(line)
    return newline.join(ret_lines)


def find_section(section_name: str, string_to_be_searched, section_re_template: str = SECTION_RE_TEMPLATE,
                 return_match=False, start_pos=0):
    section_re = section_re_template.format(section_name)
    compiled_regex = re.compile(section_re, re.MULTILINE)
    if return_match:
        return compiled_regex.search(string_to_be_searched, start_pos)
    else:
        return compiled_regex.search(string_to_be_searched, start_pos).group(0)


if __name__ == '__main__':
    from dihedral_validator.input import read_input_file
    params = read_input_file(os.path.join('example', 'input'))
    print(params)
    created_dihedraltypes = create_dihedraltypes({'CT-CT-CT-OS': [1, 2, 3, 4], 'CT-CT-OS-CT': [2, 3, 4, 5, 6, 7]})
    print('------------------------------')
    print(created_dihedraltypes)
    print('------------------------------')
    print(substitute_comment(created_dihedraltypes, 'huj dupa\nkurwa cipa'))
    #print(parse_itp_file(os.path.join('example', 'gromacs_specific_files', 'triacetin_qqAWA_q1_new_t3t4.itp'), {}))
    # TODO program i data puszczania tej analizy w dihedraltypes + dodatki (ładunki czy coś) - czyli zrobienie dihedraltypes od zera
    # TODO ale program jest przez jakiś wyższy skrypt ustawiany