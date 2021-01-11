import argparse
import multiprocessing
import os
import sys

from joblib import Parallel, delayed
from tqdm import tqdm

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")

parser = argparse.ArgumentParser()
#Required Arguments
parser.add_argument('directory', type=str, help="Folder with data")
parser.add_argument('wildcard', type=str, help="file wirldcard")

print("THIS IS AT THE MOMENT HARDCODED TO CONVERT TO UTM32N WGS84")

try:
    options = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

args = parser.parse_args()
args.directory.strip("/")
print("TIF warnings are supressed")

def getfiles(ID='', PFAD='.'):
    # Gibt eine Liste mit Dateien in PFAD und der Endung IDENTIFIER aus.
    files = []
    for file in os.listdir(PFAD):
        if file.endswith(ID):
            files.append(str(file))
    return files


filelist = getfiles(args.wildcard, args.directory)

def convert_to_UTM(directory, image, suffix):
    image_out = os.path.basename(image)
    image_out = image_out.strip(suffix)
    image_out = image_out + '_UTM32NWGS84.tif'
    cmd = 'gdalwarp -t_srs \'+proj=utm +zone=11 +datum=WGS84\' -overwrite ' + '"' + directory + '/' + image + '"' + ' "' + directory + '/' + image_out + '"'
    #print(cmd)
    os.system(cmd)
    return


Parallel(n_jobs=num_cores)(delayed(convert_to_UTM)(args.directory, image, args.wildcard) for image in tqdm(filelist))
