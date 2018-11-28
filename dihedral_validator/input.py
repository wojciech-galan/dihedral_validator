#! /usr/bin/python
# -*- coding: utf-8 -*-
import yaml


def read_input_file(path: str):
    with open(path, 'r') as f:
        return yaml.load(f)


if __name__ == '__main__':
    import os

    print(read_input_file(os.path.join('example', 'input')))
