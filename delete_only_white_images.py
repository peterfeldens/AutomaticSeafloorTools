# !/usr/bin/env python
# coding: utf8

# check for images that are only white and delete these images
# white is defined for everything more than >250 on average in brightness

import argparse
import multiprocessing
import os

import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm
import automatic_seafloor_functions as asf
from PIL import Image

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")

parser = argparse.ArgumentParser()

# Required Arguments
parser.add_argument('source_directory', type=str, help="Folder with input mosaics")
parser.add_argument('wildcards', type=str, help="identfiy the files")
parser.add_argument('threshold', type=float, help="Threshold, above is considered white. Range 0-1", default=255)


args = asf.parse_args(parser)
args.source_directory.strip("/")

files = asf.getfiles(args.wildcards, args.source_directory)
print('Working on ', len(files), ' files.')
orig = len(files)

def delete_white(file, folder):
    img = np.asarray(Image.open(folder + "/" + file))
    if np.mean(img) > args.threshold:
        cmd = 'rm' + '  ' + args.source_directory + '/' + file
        os.system(cmd)

after = len(files)
Parallel(n_jobs=num_cores)(delayed(delete_white)(file, args.source_directory) for file in tqdm(files))

print(orig - after, " files of ", orig, " have been deleted.")
