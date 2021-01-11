"""
#check for images that are only black and delete these images
# white is defined for everything more than <5  on average in brightness
"""
import argparse
import multiprocessing
import os

import numpy as  np
import skimage
from joblib import Parallel, delayed
from tqdm import tqdm

import automatic_seafloor_functions as asf

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")

PARSER = argparse.ArgumentParser()

# Required Arguments
PARSER.add_argument('source_directory', type=str, help="Folder with input mosaics")
PARSER.add_argument('wildcards', type=str, help="identfiy the files")
PARSER.add_argument('threshold', type=float, help="Threshold, below  is considered black. Range 0-1", default=0)



def delete_black(file):
    img = skimage.io.imread(args.source_directory + '/' + file, as_gray=True)
    if np.mean(img) < args.threshold:
        cmd = 'rm' + '  ' + args.source_directory + '/' + file
        os.system(cmd)
    return


args = asf.parse_args(parser)
args.source_directory.strip("/")

files = asf.getfiles(args.wildcards, args.source_directory)
print('Working on ', len(files), ' files.')

Parallel(n_jobs=num_cores)(delayed(delete_black)(file) for file in tqdm(files))
