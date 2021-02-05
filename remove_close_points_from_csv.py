import argparse

import numpy as np
import pandas as pd
import automatic_seafloor_functions as asf

print("Assuming projected coordinates in meters in column X and Y of input file")

parser = argparse.ArgumentParser()

parser.add_argument('in_path', type=str, help="Path to csv file")
parser.add_argument('out_path', type=str, help="Path to out csv file")
parser.add_argument("-b", "--boundary_threshold", type=float,
                    help="Stones closer together will be merged", default=0.5)
parser.add_argument("-s", "--separator", type=str,
                    help="separator of csv", default=",")

args = asf.parse_args(parser)
boundary_threshold = args.boundary_threshold

df = pd.read_csv(args.in_path, sep=args.separator)
print('Entferne Koordinaten mit Entfernunge < als: ', boundary_threshold)
merge_list = []
for row in df.itertuples():
    # bounds return (minx, miny, maxx, maxy)
    x = row.X
    y = row.Y
    near_points = df[
        (np.abs(df.X.values - x) < boundary_threshold) & (np.abs(df.Y.values - y) < boundary_threshold)].index
    merge_list.append([near_points])

# quick and dirtz: delete all antries except first
for element in merge_list:
    to_del = element[1:]
    try:
        df = df.drop(labels=to_del)
    except Exception as ex:
        print(ex)
        continue

df.to_csv(args.out_path)
