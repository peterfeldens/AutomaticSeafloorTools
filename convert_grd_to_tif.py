import argparse
import multiprocessing
import os

from joblib import Parallel, delayed

import automatic_seafloor_functions as asf

num_cores = multiprocessing.cpu_count() - 1

print("Using ", num_cores, " cores. ")
parser = argparse.ArgumentParser()

parser.add_argument('directory', type=str, help="Folder with input grids")


def execute_command(command):
    print("Execute: ", command)
    os.system(command)
    return


args = asf.parse_args(parser)
args.directory.strip("/")

file_list = asf.getfiles(".grd", args.directory)

Parallel(n_jobs=num_cores)(delayed(execute_command)(
    'gdal_translate -of GTiff ' + args.directory + "/" + str(grid) + ' ' + args.directory + "/" + str(grid) + '.tiff')
                           for grid in file_list)
