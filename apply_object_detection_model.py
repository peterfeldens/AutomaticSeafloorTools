#!/usr/bin/env python
# coding: utf8

"""After training the model, run it over the list of file, extract the boxes and scores and labels, convert back to
real coordinates, and save as csv

This one works on small tiles, only considering the backscatter and not spatial information.

It is much faster though. 

"""
# import keras

import argparse
import glob

import numpy as np
import pandas as pd
# import miscellaneous modules
# set tf backend to allow memory to grow, instead of claiming everything
# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from tqdm import tqdm

import automatic_seafloor_functions as asf

parser = argparse.ArgumentParser()
# Required Arguments
parser.add_argument('raster', type=str, help="Folder with data")
parser.add_argument('model_path', type=str, help="Path to model file")
parser.add_argument('output', type=str, help="Path and name of result")

parser.add_argument("-f", "--format", type=str,
                    help="Format of image tiles", default='tif')
parser.add_argument("-m", "--minside", type=int,
                    help="Image size minimum side", default=800)
parser.add_argument("-d", "--detection_threshold", type=float,
                    help="Minimum score reported", default=0.2)


labels_to_names = {0: 'stone'}

args = asf.parse_args(parser)
args.raster.strip("/")


# main1
image_folder = args.raster
image_type = args.format
model_path = args.model_path
min_side = args.minside
output = args.output
detection_threshold = args.detection_threshold  # include detections with accuracy above
# all


convert_model = 'yes'


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
                 'lrx': box_lrx_coord, 'lry': box_lry_coord, 'X': box_mean_x, 'Y': box_mean_y, 'WKT': str(
                    'POLYGON ((' + str(box_ulx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(
                        box_lry_coord) + ',' + str(box_lrx_coord) + ' ' + str(box_lry_coord) + ',' + str(
                        box_lrx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(
                        box_uly_coord) + '))')}))

    # wegschreiben
    df = pd.DataFrame(results)

    print("Berechne bounding box Fläche unter der Annahme vom projizierten Koordinates")
    df['Area_bounding_box'] = np.abs((df.uly - df.lry)) * np.abs((df.ulx - df.lrx))

    print(df.head)
    df.to_csv(output, index=False)


main()
