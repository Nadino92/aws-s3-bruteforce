#!/usr/bin/env python
from glob import glob
import os 
cur_dir = os.path.dirname(os.path.realpath(__file__))

def get_previous_scans():
    """Returns an array of all previously scanned files"""
    previously_scanned = []
    file_names = glob("{cur_dir}/scanned/*.txt".format(cur_dir=cur_dir))
    for file_name in file_names:
        previously_scanned.extend(get_strings(file_name))
    return previously_scanned


def get_strings(file_name):
    """Returns and array of strings from a file, where each line is an item"""
    strings = []
    with open(file_name, 'r') as f:
        for line in f:
            if line.strip():
                strings.append(line.strip())
    return strings

