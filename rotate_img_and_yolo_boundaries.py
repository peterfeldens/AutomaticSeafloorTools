#Rotate all images for which a txt file exists
from tqdm import tqdm
import os
import argparse
import sys

parser = argparse.ArgumentParser()

# Required Arguments
parser.add_argument('--image_directory', type=str, help="Folder with input mosaics")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

# Strip '/'
args.image_directory.strip("/")


angles = [45,90,135,180,225,270,325]  #in degrees

def getfiles(ID='', PFAD='.', rekursive='no'):
    # Gibt eine Liste mit Dateien in PFAD und der Endung IDENTIFIER aus.
    import os
    import glob2
    files = []
    if rekursive == 'no':
        for file in os.listdir(PFAD):
            if file.endswith(ID):
                files.append(str(file))
    if rekursive == 'yes':
        files = glob2.glob(PFAD + '/**/*' + ID)
    return files


files = getfiles('txt', args.image_directory)
for f in tqdm(files):
    for a in angles:
        filename = os.path.basename(f)
        basename = os.path.splitext(filename)[0]
        filename = args.image_directory + basename + ".jpg"
        cmd = 'python  /content/drive/MyDrive/repos/Yolo_bbox_manipulation/rotate.py -i ' + filename + ' -a ' +  a
        os.system(cmd)