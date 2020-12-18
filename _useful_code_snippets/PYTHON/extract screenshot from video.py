#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Export video snapshots

@author: peter
"""

import cv2
import pandas as pd
import itertools

def getfiles(ID='.mp4', PFAD='.'):
    # Gibt eine Liste mit Dateien in PFAD und der Endung IDENTIFIER aus.
    import os
    files = []
    for file in os.listdir(PFAD):
        if file.endswith(ID):
            files.append(str(file))
    return files

def extract_Images(filename):
    result = []
    count = 0
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count * 1000))
        success, image = vidcap.read()
        result.append([filename + "_" + str(count) + ".jpg", filename, count])
        #cv2.imwrite(filename + "_" + str(count) + ".jpg", image)
        count = count + 3
    return result 

list_of_filename_and_duration = []
files = getfiles()
for video in files:
    print("Working on: ", video)
    result = extract_Images(video)
    list_of_filename_and_duration.append(result)

merged = list(itertools.chain(*list_of_filename_and_duration))

df = pd.DataFrame(merged)

df.to_csv('list_of_frames_with_duration.csv', sep =',')