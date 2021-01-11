#!/usr/bin/env python
# coding: utf8
"""
Create tf datasets from the training and validation image folders
"""

import argparse
import multiprocessing
import os

from joblib import Parallel, delayed
from tqdm import tqdm

import automatic_seafloor_functions as asf


def make_png(directory, image):
    cmd = 'mogrify -quiet -format png ' + '"' + directory + '/' + image + '"'
    os.system(cmd)
    return


def main():
    num_cores = multiprocessing.cpu_count() - 1
    print("Using ", num_cores, " cores. ")

    parser = argparse.ArgumentParser()
    # Required Arguments
    parser.add_argument('directory', type=str, help="Folder with data")

    args = asf.parse_args(parser)

    args.directory.strip("/")
    print("TIF warnings are supressed")

    filelist = asf.getfiles('.tif', args.directory)

    Parallel(n_jobs=num_cores)(delayed(make_png)(args.directory, image) for image in tqdm(filelist))


main()
