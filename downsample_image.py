#!/usr/bin/env python
# coding: utf8
"""
Downsample images to create input data for superresolustion training data
"""
import argparse
import multiprocessing

from joblib import Parallel, delayed
from tqdm import tqdm

import automatic_seafloor_functions as asf

parser = argparse.ArgumentParser()

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")

# Required Arguments
parser.add_argument('source_directory', type=str, help="Folder with input mosaics")
parser.add_argument('target_directory', type=str, help="Target folder for image files")
parser.add_argument('factor', type=int, help="downsampling factor")
parser.add_argument('wildcards', type=str, help="identfiy the files")


def downsample_image(folder, image_name, factor, target_folder):
    from skimage.transform import rescale
    from skimage.io import imsave
    from skimage.io import imread

    image = folder + '/' + image_name
    img = imread(image)

    img_down = rescale(img, 1 / factor)

    # img_down = img_down.astype(np.uint8)  # convert to greyscale
    # img_up = rescale(img_down, factor)

    imsave(target_folder + '/' + image_name, img_down)
    return


args = asf.parse_args(parser)
args.source_directory.strip("/")
args.target_directory.strip("/")

files = asf.getfiles(args.wildcards, args.source_directory)

print("Working on ", len(files), "images")

Parallel(n_jobs=num_cores)(
    delayed(downsample_image)(args.source_directory, file, args.factor, args.target_directory) for file in tqdm(files))
