#!/usr/bin/env python
# coding: utf8
"""
Add suffix to filename
"""

import argparse
import os

from tqdm import tqdm

import automatic_seafloor_functions as asf

parser = argparse.ArgumentParser()
# Required Arguments
parser.add_argument('directory', type=str, help="Folder with data")
parser.add_argument('wildcards', type=str, help="identifier for Files")
parser.add_argument('suffix', type=str, help="remove suffix before wildcard")

args = asf.parse_args(parser)

file_list = asf.getfiles(args.wildcards, args.directory)

for file in tqdm(file_list):
    file_base = file.strip(args.wildcards)
    file_base = file_base.strip(args.suffix)
    file_new = file_base + args.wildcards
    cmd = 'cp ' + args.directory + '/' + file + ' ' + args.directory + '/' + file_new
    os.system(cmd)
