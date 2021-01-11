#!/usr/bin/env python
# coding: utf8
"""
Check folder for correct tile size of images and delete those that dont fit
"""

import argparse
import os

from osgeo import gdal
from tqdm import tqdm

import automatic_seafloor_functions as asf

parser = argparse.ArgumentParser()
# Required Arguments
parser.add_argument('directory', type=str, help="Folder with data")
parser.add_argument('tiles', type=int, help="tile size of images")
parser.add_argument('wildcards', type=str, help="identifier for Files")

args = asf.parse_args(parser)
args.directory.strip("/")

print("TIF warnings are supressed")

file_list = asf.getfiles(args.wildcards, args.directory)

counter = 0
for image in tqdm(file_list):
    img = args.directory + '/' + image
    rds = gdal.Open(img)
    img_width, img_height = rds.RasterXSize, rds.RasterYSize
    if not img_width == args.tiles:
        cmd = 'rm ' + img
        os.system(cmd)
        counter = counter + 1
    if not img_height == args.tiles:
        cmd = 'rm ' + img
        os.system(cmd)
        counter = counter + 1
print("A total of ", counter, " files have been deleted ( ", counter / len(file_list) * 100, " Percent.")
