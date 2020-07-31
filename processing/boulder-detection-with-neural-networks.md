---
description: 'Author: Peter Feldens'
---

# Object detection with Neural networks

In this chapter, it is attempted to provide a complete step-by-step tutorial on how to train and apply a neural network to detect objects \(in this case boulders\) in backscatter mosaics. 

## Software requirements

Most of the prapration and postprocessing is done by the gdal utilities, which are called from python scripts in this case. 

## Preparation of training data

### Obtain example datasets

The example dataset used in this chapter is available as supplementary data to the open access article: 

### Using QGIS for image annotation

### Preparation of training dataset

Large backscatter mosaics cannot be improted in neural networks at once. It is required to break them down into smaller mosaics that can be fed into the network for training \(and later application\). The following script create many small images from a large mosaic. 

```python
import os
import sys
import argparse
import glob
from tqdm import tqdm
import gdal

parser = argparse.ArgumentParser()

#Required Arguments

parser.add_argument('source_directory', type=str, help="Folder with input mosaics")
parser.add_argument('target_directory', type=str, help="Target folder for image files")
parser.add_argument('tile_size', type=int, help="size of the squares in pixels")
parser.add_argument('wildcards', type=str, help="identfiy the files")

#Optional Arguments: Verbosity displays all commmands
parser.add_argument("-o","--overlap", type=int, help="number of overlap between pixels", default=0)

def getfiles(ID='', PFAD='.'):
    # Gibt eine Liste mit Dateien in PFAD und der Endung IDENTIFIER aus.
    files = []
    for file in os.listdir(PFAD):
        if file.endswith(ID):
            files.append(str(file))
    return files

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

args.source_directory.strip("/")
args.target_directory.strip("/")

files = getfiles(args.wildcards, args.source_directory)

skipped_files = []
for mosaic in tqdm(files):
    try:
        if args.overlap == 0:
            cmd = 'gdal_retile.py -ps ' + str(args.tile_size) + ' ' + \
            str(args.tile_size) + ' -targetDir ' + \
            '"' + args.target_directory + '"' + ' ' + \
            '"' + args.source_directory + '/' + mosaic+'"' 
            os.system(cmd)
        if args.overlap > 0:
            cmd = 'gdal_retile.py -ps ' + str(args.tile_size) + ' ' + \
            str(args.tile_size) + ' -overlap ' + str(args.overlap) + \
            ' -targetDir ' + '"' + args.target_directory + '"' + ' ' + \
            '"' +  args.source_directory + '/' + mosaic+'"' 
            os.system(cmd)

    except:
        skipped_files.append(mosaic)

#List of files that do not work
if skipped_files:
    print('Skipped Files:', skipped_files)
    print('Most likely these mosaics include more than 1 band. Convert to true grayscale images.')
```



## Training the model

## Application of the model

### prepare the data

### run the model

### Loading results in QGIS

