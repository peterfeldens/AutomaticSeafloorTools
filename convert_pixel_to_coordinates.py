#this s only works with UTM coordinates.
# Format of csv file
# example:
# H:\Workspace\TensorFlow\workspace\15m_subset\VirtualImage_09_04.tif,88,74,97,83,Stone
# path, x1, y1, x2, y2 and class_name

import pandas as pd
import automatic_seafloor_functions as asf
import argparse
import os

parser = argparse.ArgumentParser()
# Required Arguments
parser.add_argument('directory_tifs', type=str, help="Folder with image data")
parser.add_argument('csv', type=str, help="csv file with pixel coordinates")
parser.add_argument('csv_out', type=str, help="name of file with converted coordinates")
parser.add_argument('--convert_utm', help="Convert images to utm", action='store_true')
parser.add_argument('--create_tfw', help="Create World Files for images", action='store_true')


args = asf.parse_args(parser)
args.directory_tifs.strip("/")

image_dir = args.directory_tifs  # Change if applicable
csv_path = args.csv  # assumes CSV column as above
csv_out = args.csv_out

if args.convert_utm:
    print("Look at the script reproject_coordinates.py")

if args.create_tfw:
    cmd = "python create_tfw.py " + image_dir + " tif 1 tfw"
    print("Create the tfw files using this command")
    print(cmd)


df = pd.read_csv(csv_path, names=['image_path', 'classname', 'x1', 'y1', 'x2', 'y2' ])

df[['x1_coord','y1_coord', 'x2_coord', 'y2_coord', 'box_mean_x', 'box_mean_y']] = [asf.convert_pixel_to_real(img, box) for img, box in zip(df['image_path'], zip(df.x1, df.y1, df.x2, df.y2))]

#df[['x1_coord','y1_coord', 'x2_coord', 'y2_coord', 'box_mean_x', 'box_mean_y']] = df.result.str.split(",",expand=True,)

df['wkt'] =  [str('POLYGON ((' + str(x1) + ' ' + str(y1) + ',' + str(x1) + ' ' +
    str(y2) + ',' + str(x2) + ' ' + str(y2) + ',' +
    str(x2) + ' ' + str(y1) + ',' + str(x1) + ' ' +
    str(y1) + '))') for x1, y1, x2, y2 in zip(df.x1_coord,df.y1_coord, df.x2_coord, df.y2_coord)]

print(df.head)

#df['wkt'] =  str('POLYGON ((' + str(box_ulx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(
#        box_lry_coord) + ',' + str(box_lrx_coord) + ' ' + str(box_lry_coord) + ',' + str(
#        box_lrx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(
#        box_uly_coord) + '))')}))


df.to_csv(csv_out, columns=['box_mean_x', 'box_mean_y', 'wkt', 'classname'])

