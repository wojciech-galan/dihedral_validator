#! /usr/bin/python
# -*- coding: utf-8 -*-

import time


def create_time_str_for_filename(time_struct) -> str:
    return time.strftime('%Y_%m_%d_hour_%H_%M_%S', time_struct)
