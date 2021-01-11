import argparse

import numpy as np
from skimage import exposure
from skimage import io
from tqdm import tqdm

import automatic_seafloor_functions as asf

"""
Example use 
hist_stretch.py /Path/to/folder tif recursive
histogram stretches all tif files in folder and subfolders 
"""

parser = argparse.ArgumentParser()

# Required Arguments
parser.add_argument('source_directory', type=str, help="Folder with input mosaics")
parser.add_argument('wildcards', type=str, help="identfiy the files")
parser.add_argument('recursive', type=str, help="identfiy the files", default="no")

args = asf.parse_args(parser)
args.source_directory.strip("/")

clip_limit = 0.1
print("Clip limit for adaptive equalization set to:", clip_limit)

clip_stretch = (2, 98)
print("Percentiles for contrast stretching set to:", clip_stretch)

if args.recursive == "recursive":
    print("Searching for files in subfolders")
    files = asf.getfiles(args.wildcards, args.source_directory, rekursive='yes')
else:
    print("Searching for files in folder:", args.source_directory)
    files = asf.getfiles(args.wildcards, args.source_directory)

# Convert
for file in tqdm(files):
    img = io.imread(file)
    # rescaled image
    p2, p98 = np.percentile(img, clip_stretch)
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))
    io.imsave(file + "_stretched.png", img_rescale, check_contrast=False)

    # hist-eq image
    img_eq = exposure.equalize_hist(img)
    io.imsave(file + "_equalization.png", img_eq, check_contrast=False)

    # adapative-histe
    img_adapteq = exposure.equalize_adapthist(img, clip_limit=clip_limit)
    io.imsave(file + "_adaptive.png", img_adapteq, check_contrast=False)
