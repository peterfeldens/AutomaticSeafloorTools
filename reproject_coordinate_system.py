import argparse
import multiprocessing
import os

from joblib import Parallel, delayed
from tqdm import tqdm

import automatic_seafloor_functions as asf

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")

parser = argparse.ArgumentParser()
# Required Arguments
parser.add_argument('directory', type=str, help="Folder with data")
parser.add_argument('wildcard', type=str, help="file wirldcard")

print("THIS IS AT THE MOMENT HARDCODED TO CONVERT TO UTM32N WGS84")

args = asf.parse_args(parser)
args.directory.strip("/")
print("TIF warnings are supressed")

file_list = asf.getfiles(args.wildcard, args.directory)


def convert_to_UTM(directory, image, suffix):
    image_out = os.path.basename(image)
    image_out = image_out.strip(suffix)
    image_out = image_out + '_UTM32NWGS84.tif'
    cmd = 'gdalwarp -t_srs \'+proj=utm +zone=11 +datum=WGS84\' -overwrite ' + '"' + directory + '/' + image + '"' + ' "' + directory + '/' + image_out + '"'
    # print(cmd)
    os.system(cmd)
    return


Parallel(n_jobs=num_cores)(delayed(convert_to_UTM)(args.directory, image, args.wildcard) for image in tqdm(file_list))
