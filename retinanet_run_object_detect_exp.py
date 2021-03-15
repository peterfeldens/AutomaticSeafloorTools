
import keras

# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time
from tqdm import tqdm

import tensorflow as tf
from shapely.geometry import Point
import pandas as pd
import glob
import os, gdal
import os.path
import shutil

def get_boundaries(image):
    '''
    Bestimmen der Bildgrenzen
    '''
    src = gdal.Open(image)
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    return ulx, xres, uly, yres, lrx, lry


def convert_pixel_to_real(image, box):
    # box : A list of 4 elements (x1, y1, x2, y2).
    ulx, xres, uly, yres, lrx, lry = get_boundaries(image)
    box_ulx = box[0]
    box_uly = box[1]
    box_lrx = box[2]
    box_lry = box[3]

    assert yres < 0   #otherwise, upper left is not the origin of the image

    # Convert pixel to real
    box_ulx_coord = ulx + (box_ulx * xres)
    box_uly_coord = uly + (box_uly * yres) #yres ist negativv
    box_lrx_coord = ulx + (box_lrx * xres)
    box_lry_coord = uly + (box_lry * yres)
    box_mean_x = (box_ulx_coord + box_lrx_coord) /2
    box_mean_y = (box_uly_coord + box_lry_coord) /2

    return box_ulx_coord, box_uly_coord, box_lrx_coord, box_lry_coord, box_mean_x, box_mean_y

################################################################################
base_folder =  '/media/peter/Daten_1/EXPERIMENT'
os.chdir(PATH)
"""
The following folder should be present in PATH

./to_be_processed Place tifs to be processed here
./ empty folder where tiles will be created
./ snapshots
./ raw backup folder with raw data, not needed by script
./ output results files will be placed here
./ models model files should be stored here
./ keras_retinanet the git archive of keras retinanet should be here and installed
./ input emptz folder used for copzing files
./ AutoMaticSeafloor tools. The ASF tools should be gitted here\
./ already_processed  finished tifs will be copie dhere from the to_be_processed folder
"""

image_folder = './tiles/'

image_type = '.tif'
output_folder = './output/'
output = 'resnet50_csv_SR100_17_r09_100in_800pixels_no_srres.csv'
labels_to_names = {0: 'stone'}
model_path = os.path.join('.models/resnet50_csv_SR100_17_r09.h5')
convert_model = 'yes'
detection_threshold = 0.15  #include detections with accuracy above
min_side=800
boundary_threshold = 1  #Stones smaller together will be merged
################################################################################
# Make filelist of all input
input_img = glob.glob(os.path.join('./to_be_processed', "*.tif"))

error_list = []

# copy and prepare one file
for f in tqdm(input_img):
    #move to input
    print('Copy input')
    shutil.copyfile(f, './input/' + os.path.basename(f))
    #copz eventual tfw and prj
    f_nosuff = os.path.splitext(f)[0]
    try:
        shutil.copyfile(f_nosuff + '.tfw', './input/' + os.path.basename(f_nosuff) + '.tfw')
        shutil.copyfile(f_nosuff + '.prj', './input/' + os.path.basename(f_nosuff) + '.prj')
    except:
        print("Input file without tfw")


    ##Convert to singleband greyscale if needed
    print('Convert to greyscale')
    command = 'python ./AutomaticSeafloorTools/convert_to_greyscale.py ./input ./input .tif --tag temp --overwrite'
    os.system(command)


    ## CUT MOSAIC INTO TILES
    print('Cut to tiles')
    command = 'python ./AutomaticSeafloorTools/cut_image_to_tiles.py ./input ./tiles/ 100 .tif'
    os.system(command)

    ## TEST: Remove files smaller 1 kb, which will be background
    print('Remove empty files')
    tile_img = []
    tile_img = glob.glob(os.path.join('./tiles/', "*.tif"))
    deleted_img = 0
    for tile in tile_img:
        if os.path.getsize(tile) < 2 * 1024:
            os.remove(tile)
            deleted_img = deleted_img +1
    print("deleted number of images due to small size: ", deleted_img)




    ## CREATE WORLD FILES FOR IMAGW TILES
    print('Create world files')
    command = 'python ./AutomaticSeafloorTools/generate_tfw.py ./tiles/ .tif 1 .tfw'
    os.system(command)# analyze one file


    ## Run the model
    print('Run model')
    # load retinanet model
    model = models.load_model(model_path, backbone_name='resnet50')

    # if the model is not converted to an inference model, use the line below
    if convert_model == 'yes':
        model = models.convert_model(model)

    #print(model.summary())

    # load label to names mapping for visualization purposes
    labels_to_names = {0: 'stone'}

    # get image list
    image_list = glob.glob(image_folder + '*' + image_type)
    print(image_list)

    #iterate over list
    results = []
    print("Working on Folder ", image_folder)
    for img in tqdm(image_list):
        try:
            #start = time.time()
            image = read_image_bgr(img)
            image = preprocess_image(image)
            image, scale = resize_image(image, min_side = min_side)

            boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
            #print("processing time: ", time.time() - start)

            # correct for image scale
            boxes /= scale

            #get coordinates
            for box, score, label in zip(boxes[0], scores[0], labels[0]):
                # scores are sorted so we can break
                if score < detection_threshold:
                    break
                box_ulx_coord, box_uly_coord, box_lrx_coord, box_lry_coord, box_mean_x, box_mean_y  = convert_pixel_to_real(img, box)

                results.append(dict({'image' : img, 'class' : label, 'score' : score, 'ulx': box_ulx_coord, 'uly' : box_uly_coord , 'lrx' : box_lrx_coord, 'lry' : box_lry_coord, 'x': box_mean_x, 'y' : box_mean_y , 'WKT': str('POLYGON ((' + str(box_ulx_coord) + ' ' + str(box_uly_coord) + ',' +  str(box_ulx_coord) + ' ' + str(box_lry_coord) + ',' + str(box_lrx_coord) + ' ' + str(box_lry_coord) + ',' + str(box_lrx_coord) + ' ' + str(box_uly_coord) + ',' + str(box_ulx_coord) + ' ' + str(box_uly_coord) + '))') }))
        except:
            print("Error in image ", img , "of file ", f)
            error_list.append("Error in image ", img , "of file ", f)

    #wegschreiben
    try:
        df = pd.DataFrame(results)
    except:
        continue

    #print('Entferne Koordinaten mit Entfernunge < als: ', boundary_threshold)
    merge_list = []
    for row in df.itertuples():
        #bounds return (minx, miny, maxx, maxy)
        idx = row.Index
        x = row.x
        y = row.y
        near_points = df[(np.abs(df.x.values - x) < boundary_threshold ) & (np.abs(df.y.values - y) < boundary_threshold )].index
        merge_list.append(near_points)

        # df.loc[merge_list[element]].agg({'class':'mean', 'lrx':'mean'}) # so koennte man die Mittelwerte ausrechnen
    # quick and dirtz: delete all antries except first
    for element in merge_list:
        to_del = element[1:]
        try:
            df.drop(labels = to_del, inplace = True)
        except:
            continue
    try:
        #print("Berechne bounding box Fläche unter der Annahme vom projizierten Koordinates")
        df['Area_bounding_box'] = np.abs((df.uly - df.lry)) * np.abs((df.ulx - df.lrx))
    except:
        print("Error in ", "np.abs((df.uly - df.lry)) * np.abs((df.ulx - df.lrx)")


    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")


    #output
    outname = output_folder + timestr + '_' + os.path.basename(f) + '_' + output
    df["modelpath"] = model_path
    df.to_csv(outname, index = None)
    shutil.copyfile(outname, '/media/peter/Linux/IOW Marine Geophysik Dropbox/Sandbox/peter/' + os.path.basename(outname))


    ## move tif to processed
    print('Move')
    shutil.move('./input/' + os.path.basename(f), './already_processed/' + os.path.basename(f))
    try:
        shutil.move('./input/' + os.path.basename(f_nosuff) + '.tfw', './already_processed/' + os.path.basename(f_nosuff) + '.tfw')
        shutil.move('./input/' + os.path.basename(f_nosuff) + '.prj', './already_processed/' + os.path.basename(f_nosuff) + '.prj')
    except:
        print("Input file without tfw")
    #Clean up
    #print('Clean up')
    filelist = glob.glob(os.path.join('./tiles', "*.tif"))
    for f in filelist:
        os.remove(f)
    filelist = glob.glob(os.path.join('./tiles', "*.tfw"))
    for f in filelist:
        os.remove(f)
    filelist = glob.glob(os.path.join('./tiles', "*.prj"))
    for f in filelist:
        os.remove(f)

print(error_list)
