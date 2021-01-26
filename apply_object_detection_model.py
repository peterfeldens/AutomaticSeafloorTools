#!/usr/bin/env python
# coding: utf8

"""After training the model, run it over the list of file, extract the boxes and scores and labels, convert back to
real coordinates, and save as csv """
# import keras

import glob

import gdal
import geopandas as gpd
import numpy as np
import pandas as pd
import shapely.geometry as geom
# import miscellaneous modules
# set tf backend to allow memory to grow, instead of claiming everything
# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from shapely.geometry import Point, LineString
from tqdm import tqdm

import automatic_seafloor_functions as asf
# Really crude importing
from apply_object_detect_config_file import *

parser = argparse.ArgumentParser()
# Required Arguments
parser.add_argument('raster', type=str, help="Folder with data")
parser.add_argument('block_x', type=int, help="tile size of images")
parser.add_argument('model_path', type=str, help="identifier for Files")

args = asf.parse_args(parser)
args.directory.strip("/")

raster = args.raster
block_x = args.block_x
model_path = args.model_path

def main():
    # load retinanet model
    model = models.load_model(model_path, backbone_name='resnet50')

    # if the model is not converted to an inference model, use the line below
    if convert_model == 'yes':
        model = models.convert_model(model)

    # get image list
    image_list = glob.glob(image_folder + '*' + image_type)
    print(image_list)

    # iterate over list
    results = []
    print("Working on Folder ", image_folder)
    for img in tqdm(image_list):
        # start = time.time()
        image = read_image_bgr(img)
        image = preprocess_image(image)
        image, scale = resize_image(image, min_side=min_side)

        boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
        # print("processing time: ", time.time() - start)

        # correct for image scale
        boxes /= scale

        # get coordinates
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            # scores are sorted so we can break
            if score < detection_threshold:
                break
            box_ulx_coord, box_uly_coord, box_lrx_coord, box_lry_coord, box_mean_x, box_mean_y = asf.convert_pixel_to_real(
                img, box)

            results.append(dict(
                {'image': img, 'class': label, 'score': score, 'ulx': box_ulx_coord, 'uly': box_uly_coord,
                 'lrx': box_lrx_coord, 'lry': box_lry_coord, 'x': box_mean_x, 'y': box_mean_y, 'WKT': str(
                    'POLYGON ((' + str(box_ulx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(
                        box_lry_coord) + ',' + str(box_lrx_coord) + ' ' + str(box_lry_coord) + ',' + str(
                        box_lrx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(
                        box_uly_coord) + '))')}))

    # wegschreiben
    df = pd.DataFrame(results)

    print('Entferne Koordinaten mit Entfernunge < als: ', boundary_threshold)
    merge_list = []
    for row in df.itertuples():
        # bounds return (minx, miny, maxx, maxy)
        x = row.x
        y = row.y
        near_points = df[
            (np.abs(df.x.values - x) < boundary_threshold) & (np.abs(df.y.values - y) < boundary_threshold)].index
        merge_list.append(near_points)

        # df.loc[merge_list[element]].agg({'class':'mean', 'lrx':'mean'}) # so koennte man die Mittelwerte ausrechnen
    # quick and dirtz: delete all antries except first
    for element in merge_list:
        to_del = element[1:]
        try:
            df.drop(labels=to_del, inplace=True)
        except Exception as ex:
            print(ex)
            continue

    print("Berechne bounding box Fläche unter der Annahme vom projizierten Koordinates")
    df['Area_bounding_box'] = np.abs((df.uly - df.lry)) * np.abs((df.ulx - df.lrx))

    print(df.head)
    df.to_csv(output, index=None)


def pixel2coord(col, row):
    """Returns global coordinates to pixel center using base-0 raster index"""
    #ulx, xres, xskew, uly, yskew, yres
    xp = a * col + b * row + a * 0.5 + b * 0.5 + c
    yp = d * col + e * row + d * 0.5 + e * 0.5 + f
    return(xp, yp)
# load retinanet model
model = models.load_model(model_path, backbone_name='resnet50')

# if the model is not converted to an inference model, use the line below
if convert_model == 'yes':
    model = models.convert_model(model)

band_number = 1 # band number of tif to use
column_names_of_csv = ['Latitude', 'Longitude', 'filename']  # File Format of Nadir file

#read Raster
ds = gdal.Open(raster)  #open tif
band = ds.GetRasterBand(band_number)  #read first band assuming to include the BS data
# unravel GDAL affine transform parameters to get back coordinates

a, b, c, d, e, f = ds.GetGeoTransform()

max_width,max_height=ds.RasterXSize,ds.RasterYSize
x_runs=list(range(0,max_width - block_x, block_x))
y_runs=list(range(0,max_height - block_x, block_x))

results = []
for width_index in tqdm(x_runs):
    for height_index in y_runs:
        grey_array = band.ReadAsArray(width_index, height_index, block_x, block_x)  #the subset image with the specified channel
        # damit habe ich band 1. jetzt muss die entfernung jedes pixels (bzw seiner coordinaten) zu einer linie dazu
        # hier ist der offset noch nicht berücksichtigt
        pixel_coordinates = np.array([pixel2coord(xi[0][0], xi[0][1]) for xi in np.ndenumerate(grey_array)])
        #make geopandas series
        gpd_pixel_coordinates = gpd.GeoSeries([geom.Point(row[0], row[1]) for row in pixel_coordinates])

        # Read Nadir
        temp = pd.read_csv('test', sep = ',', names = column_names_of_csv)
        geometry = [Point(xy) for xy in zip(temp.Longitude, temp.Latitude)]
        df_lines = gpd.GeoDataFrame(temp, geometry=geometry)
        df_lines = df_lines.groupby(['filename'])['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else x.tolist())

        # Get distance to Nadir for each Pixel
        min_dist = np.empty(len(gpd_pixel_coordinates))
        for i, point in enumerate(gpd_pixel_coordinates):
            min_dist[i] = np.min([point.distance(line) for line in df_lines])

        # auf 0-255 skalieren
        min_dist = ((min_dist - np.min(min_dist)) / (np.max(min_dist) - np.min(min_dist))) * 255
        min_dist = np.round(min_dist).astype(int)

        # add min dist to grey_image as band
        min_dist = min_dist.reshape(block_x,block_x) # reshape to block_x, block_x (nur Quadrate)

        merge = np.dstack((grey_array, min_dist))

        #add texture or second bs channel? -> for now using the same channel twice
        image = np.dstack((merge, grey_array))

        # Super-resolution?
        #TODO

        # pass to retinanet

        # Resize and run model
        image, scale = resize_image(image, min_side=min_side)

        boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))


        # correct for image scale
        boxes /= scale

        # get coordinates
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            # scores are sorted so we can break
            if score < detection_threshold:
                break

            # Das sind die Bild-Pixel einer detektierten Bounding Box
            # die coordinaten des grey arrays stehen in pixel_coordinates..ich meine y zuerst #TODO #WICHTIG
            box_ulx = box[0]
            box_uly = box[1]
            box_lrx = box[2]
            box_lry = box[3]

            #
            x_coordinates = pixel_coordinates[:,:,1].reshape(block_x, block_x)
            y_coordinates = pixel_coordinates[:,:,0].reshape(block_x, block_x)

            # Convert pixel to real
            box_ulx_coord = x_coordinates[box_uly, box_ulx]
            box_uly_coord = y_coordinates[box_uly, box_ulx]
            box_lrx_coord = x_coordinates[box_lry, box_lrx]
            box_lry_coord = y_coordinates[box_lry, box_lrx]
            box_mean_x = (box_ulx_coord + box_lrx_coord) /2
            box_mean_y = (box_uly_coord + box_lry_coord) /2

            results.append(dict(
                {'image': raster, 'class': label, 'score': score, 'ulx': box_ulx_coord, 'uly': box_uly_coord,
                 'lrx': box_lrx_coord, 'lry': box_lry_coord, 'x': box_mean_x, 'y': box_mean_y, 'WKT': str(
                    'POLYGON ((' + str(box_ulx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(
                        box_lry_coord) + ',' + str(box_lrx_coord) + ' ' + str(box_lry_coord) + ',' + str(
                        box_lrx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(
                        box_uly_coord) + '))')}))

# wegschreiben
df = pd.DataFrame(results)

print('Entferne Koordinaten mit Entfernunge < als: ', boundary_threshold)
merge_list = []
for row in df.itertuples():
    # bounds return (minx, miny, maxx, maxy)
    x = row.x
    y = row.y
    near_points = df[
        (np.abs(df.x.values - x) < boundary_threshold) & (np.abs(df.y.values - y) < boundary_threshold)].index
    merge_list.append(near_points)

# quick and dirtz: delete all antries except first
for element in merge_list:
    to_del = element[1:]
    try:
        df.drop(labels=to_del, inplace=True)
    except Exception as ex:
        print(ex)
        continue

print("Berechne bounding box Fläche unter der Annahme vom projizierten Koordinates")
df['Area_bounding_box'] = np.abs((df.uly - df.lry)) * np.abs((df.ulx - df.lrx))

print(df.head)
df.to_csv(output, index=None)


