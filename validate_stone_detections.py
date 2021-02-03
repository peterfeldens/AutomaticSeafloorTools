"""
Here, we want to take the output bounding boxes of the stone detection program for a set of validation
tif files, and check whether manually determined picks are located within the bounding boxes

The result is to be plotted as a confusion matrix for each of the validation mosaics.
"""

import geopandas as gpd
from geopandas.tools import sjoin
import os
import argparse
import automatic_seafloor_functions as asf

parser = argparse.ArgumentParser()

# Required Arguments
parser.add_argument('--model', type=str, help="Folder with input model to test")
parser.add_argument('--base_folder_validation', type=str, help="Folder with validation_tifs",
                    default='/content/drive/MyDrive/datasets_retina/validation')
parser.add_argument('--minside', type=int, help="Min-Size of images")
parser.add_argument('--detection_threshold', type=float, help="Minimum considered score", default=0.2)

args = asf.parse_args(parser)

validation_areas = asf.getfiles('.tif', args.base_folder_validation, rekursive='yes')
print("Working on the validation files:", validation_areas)

result_list = []
for area in validation_areas:
    reference = area.split('.tif') + ".shp"
    modelfile = area.split('.tif') + ".csv"
    # run the neural networks over the validation areas
    cmd = "python apply_object_detection.py " + area + " " + args.model + " " + modelfile + "  --detection_threshold=" + args.detection_threshold + " --minside=" + args.minside
    os.system(cmd)

    # Load the result.csv file from the neural network
    ref_point = gpd.GeoDataFrame.from_file(reference)
    model_poly = gpd.GeoDataFrame.from_file(modelfile)

    # TP und FN
    pointInPolys = sjoin(ref_point, model_poly, how='left')
    notfound_stones = pointInPolys[pointInPolys['index_right'].isnull()]
    found_stones = pointInPolys[pointInPolys['index_right'].notnull()]
    duplicate_detections = found_stones[found_stones.duplicated(['index_right'])]

    # FP: Polygon outside points
    polys_with_points = found_stones['index_right'].unique()
    polys_without_points = model_poly[~model_poly.index.isin(polys_with_points)]

    # Calculate and print confusion matrix
    true_number = len(ref_point)
    detected_number = len(model_poly)
    tp = len(found_stones) - len(duplicate_detections)
    fn = len(notfound_stones)
    # fp = bounding boxes without point
    fp = len(polys_without_points)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    F1 = 2 * tp / (2 * tp + fp + fn)

    print(precision, recall, F1)
    result_list.append([area, precision, recall, F1])

print(result_list)
