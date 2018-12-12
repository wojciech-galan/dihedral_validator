#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess


class SimpleCommandWrapper():
    def __init__(self):
        super().__init__()

    def run(self, command):
        subprocess.run(command, shell=True)