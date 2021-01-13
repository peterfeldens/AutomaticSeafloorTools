# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:01:24 2016
#Makes GLCM data from TIF files

@author: feldens



Calcualtes texture parameters from a TIF image and stores as ASCII

Add gridding of output files using gmt surface

"""

import multiprocessing
# %% Variablen eingeben
import os

import numpy as np
import pandas as pd
import skimage
from joblib import Parallel, delayed
from tqdm import tqdm

import automatic_seafloor_functions as asf

num_cores = multiprocessing.cpu_count() - 1
print("Using ", num_cores, " cores. ")


def flatten(alist):
    # flatten a nested list into a flat list
    newlist = []
    for item in alist:
        if isinstance(item, list):
            newlist = newlist + flatten(item)
        else:
            newlist.append(item)
    return newlist


def setup_dataframe():
    glcm_dataframe = pd.DataFrame({'X': [],
                                   'Y': [],
                                   'ENTROPY': [],
                                   'HOMOGENEITY': [],
                                   'DISSIMILARITY': [],
                                   'Greylevels': [],
                                   'PatchSize': [],
                                   'GLCM_Distance': []
                                   })
    return glcm_dataframe


def convert_tif_to_raster(filename, band_to_keep=0):
    from skimage import io
    imarray = io.imread(filename)
    imarray_oneband = imarray[:,:,band_to_keep]
    if imarray_oneband.max() > 255:
        imarray_oneband = (imarray_oneband - 0) / (imarray_oneband.max() ) * 255
    return imarray_oneband


# %%
# Pfad zu den TIFs Muss mit / enden
PFAD = "/Users/peter/IOW Marine Geophysik Dropbox/Paper/Large_scale_stone_mapping/data/ptg/tiles_for_texture/"
os.chdir(PFAD)

input_files = asf.getfiles(".tif", PFAD)
print(input_files)

# List of filenames
outname = '_TEXT.csv'  #

# GLCM Parameters
greylevels = [63]  # greylevels !! 0 mitzÃ¤hlen!!
glcmangles = [0, np.pi * 0.25, np.pi * 0.5, np.pi * 0.75]
# glcmangles=[0]
resolution = [10]  # in grid-Zellen
glcm_distances = [1]

normalize_0_255 = 'yes'

# Sollen die Ergenisse als Grid weggeschrieben werden?
grid_res = 1  # das ist effektiv ein faktor, mit dem die resolution der glcm parameter multipliziert wird


# %%
####Programmspezifische Funktionen und Variablen###############################
#parameter = ['ENTROPY', 'HOMOGENEITY', 'CORRELATION', 'ENERGY',
#             'CONTRAST', 'DISSIMILARITY', 'MAXPROB', 'GLCMMEAN'
#             ]  # dont change, likely breaks code
parameter = ['ENTROPY', 'HOMOGENEITY', 'DISSIMILARITY']
################################################################################
# %%



def main_loop(resolution_x, resolution_y, greylevel, glcm_distance, image):
    try:
        glcm_dataframe = setup_dataframe()
        # Ergenislisten anlegen
        glcm_results = []
        # TIF konvertieren
        imarray = convert_tif_to_raster(image)
        if imarray.mean() < 2:
            return
        if imarray.mean() > 250:
            return
        # Constant for all images - we do not want to stretch some images, and not others
        Intensity_min = 0
        Intensity_max = 255

        # scale datafile intensity to 0-greylevels
        datagrid = (imarray - Intensity_min) / (Intensity_max - Intensity_min) * greylevels

        # Padden um glat durch resolution_x bzw _y glatt teilabr zu sein. Padden mit negativen Werten (-1), die werden spÃ¤ter aussortiert
        pad_y = (int(datagrid.shape[0] / resolution_y) + 1) * resolution_y - datagrid.shape[0]
        pad_x = (int(datagrid.shape[1] / resolution_x) + 1) * resolution_x - datagrid.shape[1]
        datagrid = np.lib.pad(datagrid, [(0, pad_y), (0, pad_x)], 'constant', constant_values=(-1, -1))

        # Nan als negativ maskieren
        datagrid = np.ma.array(datagrid, mask=np.isnan(datagrid), fill_value=-1)
        datagrid = np.ma.array(datagrid, mask=-1, fill_value=-1)

        # Block windows erzeugen
        datagrid_blockview = skimage.util.view_as_blocks(datagrid, block_shape=(resolution_y, resolution_x))

        # datagrid_blockview = block_view(datagrid, block= (resolution_y, resolution_x))
        num_y = datagrid_blockview.shape[0]
        num_x = datagrid_blockview.shape[1]
        #TODO trying to make this

        for y in range(num_y):
            for x in range(num_x):
                current_subgrid = datagrid_blockview[y][x]
                if np.isnan(current_subgrid).any():
                    continue
                elif current_subgrid.min() < 0:
                    continue
                else:
                    y_index = int(y * resolution_y + resolution_y / 2)
                    x_index = int(x * resolution_x + resolution_x / 2)
                    _, _, _, _, x_coord, y_coord = asf.convert_pixel_to_real(image,
                                                                             [x_index , y_index , x_index , y_index ])
                    values = []
                    # erstellt die glcm
                    glcmdata = asf.greycomatrix(np.round(current_subgrid).astype(int), glcm_distance, glcmangles,
                                                greylevel +1)
                    # berechnet die parameter
                    for element in parameter:
                        templist = asf.greycoparameters(glcmdata, glcmangles, element)
                        values.append(templist)
                    templist = [[x_coord, y_coord, values]]
                    flattened_list = flatten(templist)
                    glcm_results.append(flattened_list)

        # nur durchfÃ¼hren wenn glcm results nicht leer ist (leeres list sind False, volle Listen sind True)
        if glcm_results:
            temp = np.array(glcm_results)
            temp_df = pd.DataFrame({'X': temp[:, 0],
                                    'Y': temp[:, 1],
                                    'ENTROPY': temp[:, 2],
                                    'HOMOGENEITY': temp[:, 3],
                                    'DISSIMILARITY': temp[:, 4],
                                    })

            # Drop negative coordinates from padding
            temp_df = temp_df[temp_df.X > 0]
            temp_df = temp_df[temp_df.Y > 0]

            if normalize_0_255 == 'yes':
                faktor = (255 - 1) + 1
                for element in parameter:
                    temp_df[element] = ((temp_df[element] - temp_df[element].min()) / (
                            temp_df[element].max() - temp_df[element].min())) * faktor

            # Daten zusammensammeln
            glcm_dataframe = glcm_dataframe.append(temp_df)

        for column in glcm_dataframe:
            if column in parameter:
                file_out = image + '_' + str(greylevel) + '_' + str(r) + '_' + str(
                    glcm_distance) + '_' + column + '_' + outname
                glcm_dataframe.to_csv(file_out, index=False, header=False, columns=['X', 'Y', column])
    except Exception as ex:
        print(ex)
        print("error in image: ", image)
        return

for greylevel in greylevels:
    for glcm_distance in glcm_distances:
        for r in resolution:
            resolution_x = r
            resolution_y = r
            Parallel(n_jobs=num_cores)(delayed(main_loop)(resolution_x, resolution_y, greylevel, glcm_distance, image)
                                       for image in tqdm(input_files))



