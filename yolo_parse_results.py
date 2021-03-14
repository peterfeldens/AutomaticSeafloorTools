import pandas as pd
import gdal
import cv2
import automatic_seafloor_functions as asf
import argparse
import sys

parser = argparse.ArgumentParser()

# Required Arguments
parser.add_argument('--directory', type=str, help="Folder with json yolor esult")
parser.add_argument('--outfile', type=str, help="result.csv")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

def f(img, x, y):
    im = cv2.imread(img)
    h, w, c = im.shape
    ulx, xres, uly, yres, lrx, lry = get_boundaries(img)

    Pixel_X = x * w
    Pixel_Y = y * h

    X = Pixel_X * xres + ulx
    Y = Pixel_Y * yres - uly

    y1 = Y - (h*yres)
    x1 = X - (w*xres)
    x2 = X + (w*xres)
    y2 = Y + (h*yres)

    return x1, y1, x2, y2


def flatten_nested_json_df(dataframe):
    dataframe = dataframe.reset_index()

    print(f"original shape: {dataframe.shape}")
    print(f"original columns: {dataframe.columns}")
    # search for columns to explode/flatten
    s = (dataframe.applymap(type) == list).all()
    list_columns = s[s].index.tolist()

    s = (dataframe.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()

    print(f"lists: {list_columns}, dicts: {dict_columns}")
    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            print(f"flattening: {col}")
            # explode dictionaries horizontally, adding new columns
            horiz_exploded = pd.json_normalize(dataframe[col]).add_prefix(f'{col}.')
            horiz_exploded.index = dataframe.index
            dataframe = pd.concat([dataframe, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns)  # inplace

        for col in list_columns:
            print(f"exploding: {col}")
            # explode lists vertically, adding new columns
            dataframe = dataframe.drop(columns=[col]).join(dataframe[col].explode().to_frame())
            new_columns.append(col)

        # check if there are still dict o list fields to flatten
        s = (dataframe[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (dataframe[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()

        print(f"lists: {list_columns}, dicts: {dict_columns}")

    print(f"final shape: {dataframe.shape}")
    print(f"final columns: {dataframe.columns}")
    return dataframe


def get_boundaries(image_tile):
    """
    Bestimmen der Bildgrenzen
    """
    src = gdal.Open(image_tile)
    ulx, xres, xskew, uly, yskew, yres = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    return ulx, xres, uly, yres, lrx, lry


df = pd.read_json(args.directory)
df = df[df['objects'].map(lambda d: len(d)) > 0]  # Filter empty lists
df = flatten_nested_json_df(df)
print(df.head())

df[['x1','y1', 'x2', 'y2']] = [f(img, x, y) for img, x,y in zip(df['filename'], df['objects.relative_coordinates.center_x'], df['objects.relative_coordinates.center_y'])]
df[['x1_coord','y1_coord', 'x2_coord', 'y2_coord', 'box_mean_x', 'box_mean_y']] = [asf.convert_pixel_to_real(img, box) for img, box in zip(df['filename'], zip(df.x1, df.y1, df.x2, df.y2))]

df['wkt'] =  [str('POLYGON ((' + str(x1) + ' ' + str(y1) + ',' + str(x1) + ' ' +
                  str(y2) + ',' + str(x2) + ' ' + str(y2) + ',' +
                  str(x2) + ' ' + str(y1) + ',' + str(x1) + ' ' +
                  str(y1) + '))') for x1, y1, x2, y2 in zip(df.x1_coord,df.y1_coord, df.x2_coord, df.y2_coord)]

print(df.head())
df.to_csv(args.outfile)