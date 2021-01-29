#!/usr/bin/env python
# coding: utf8

"""After training the model, run it over the list of file, extract the boxes and scores and labels, convert back to
real coordinates, and save as csv

This one works on small tiles, only considering the backscatter and not spatial information.

It is much faster though. 

"""
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
import argparse
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


main()


