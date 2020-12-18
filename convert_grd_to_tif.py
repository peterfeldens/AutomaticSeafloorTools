import os
import sys
import argparse
import glob
from tqdm import tqdm
import gdal
from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count() -1

print("Using ", num_cores, " cores. ")
parser = argparse.ArgumentParser()

parser.add_argument('directory', type=str, help="Folder with input grids")



def execute_command(command):
    print("Execute: ", command)
    os.system(command)
    return

def getfiles(ID='', PFAD='.'):
    # Gibt eine Liste mit Dateien in PFAD und der Endung IDENTIFIER aus.
    files = []
    for file in os.listdir(PFAD):
        if file.endswith(ID):
            files.append(str(file))
    return files

try:
    options = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

args = parser.parse_args()
args.directory.strip("/")


filelist = getfiles(".grd", args.directory)

#Parallel(n_jobs=num_cores)(delayed(execute_command)('gmt grdconvert ' +  args.directory + "/" + str(grid) +' ' + args.directory + "/"+str(grid) + '.png') for grid in filelist)
Parallel(n_jobs=num_cores)(delayed(execute_command)('gdal_translate -of GTiff ' +  args.directory + "/" + str(grid) +' ' + args.directory + "/"+str(grid) + '.tiff') for grid in filelist)

