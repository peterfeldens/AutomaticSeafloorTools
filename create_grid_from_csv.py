import argparse

import pandas as pd
import automatic_seafloor_functions as asf
import numpy as np
import os

parser = argparse.ArgumentParser()

parser.add_argument('path_csv', type=str, help="Path to csv with points to grid. Must be X,Y,I ")
parser.add_argument('output_directory', type=str, help=" folder for grid to be created")
parser.add_argument('grid_res', type=float, help="grid size")
parser.add_argument("-r", "--region", type=str, help="Manual specify region, default is from datafile", default="")
parser.add_argument("-u", "--unit", type=str, help="Units: d for degree, m for meters", default="d")

# Parse Arguments
args = asf.parse_args(parser)
args.output_directory.strip("/")
region = args.region

# Read csv
df = pd.read_csv(args.path_csv, names=['X', 'Y', 'I'])
df.sort_values(['X', 'Y'], inplace=True)
x_min = int(np.floor(df.X.min()))
x_max = int(np.ceil(df.X.max()))
y_min = int(np.floor(df.Y.min()))
y_max = int(np.ceil(df.Y.max()))

if region == "":
    region = str(str(x_min) + "/" + str(x_max) + '/' + str(y_min) + "/" + str(y_max))

print("region used is ", region)
grid_out = args.output_directory + '/' + os.path.basename(args.path_csv) + ".nc"

# GMT Method command line
if args.unit == "d":
    command = "gmt surface " + args.path_csv + " -I" + str(args.grid_res) + " -R" + region + " -G" + grid_out
    os.system(command)
if args.unit == "m":
    command = "gmt surface " + args.path_csv + " -I" + str(args.grid_res) + "e" + " -R" + region + " -G" + grid_out
    os.system(command)

# TODO
# add filtered grid options
# if filtered_grid == 'yes':
#    filtered_grid_out = str(file_out) + "_smooth.nc"
#    command = "gmt grdfilter " + grid_out + " -D0 -Fg2 " + " -G" + filtered_grid_out
#    os.system(command)
