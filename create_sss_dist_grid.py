import geopandas as gpd
import numpy as np
import pandas as pd
import fast_coord  # this is a cython file that needs to be compiled before fast_coord_setup.py build_ext --inplace
import automatic_seafloor_functions as asf
from osgeo import gdal
from shapely.geometry import Point, LineString
from tqdm import tqdm
from multiprocessing import Pool
from pygmt import surface
import argparse

parser = argparse.ArgumentParser()
tqdm.pandas()
# Required Arguments
parser.add_argument('raster', type=str, help="Path to raster mosaic in UTM coordinates with no skew")
parser.add_argument('nadir', type=str, help="Path to csv with points of nadir file and columns named X, Y and ID")
parser.add_argument('--band', type=int, help='Band number of raster to use.', default=1)
parser.add_argument('--downscale', type=int, help='Downscaling factor of tif-points', default=20)
parser.add_argument('--grid_out', type=int, help='Gridding? 0 grids original values, 1 scaled to 0-255', default=2) # currently hardcoded to 0.5 cm grid resolution
parser.add_argument('--offset', type=int, help='Maximum point-line distance to consider in meters', default=100)
parser.add_argument('--csv_out', type=int, help='Export ungridded results as csv. 1 yes, 0 is no', default=0)

args = asf.parse_args(parser)

nadir = args.nadir
raster = args.raster
downscale_factor = args.downscale
grid_input = args.grid_out
offset = args.offset
band_number = args.band
export_csv_with_raw_data = args.csv_out  # 1 export a csv file with results in folder of nadir-file


def pixel2coord(ul_x, ul_y, col, row):
    """Returns global coordinates to pixel center using base-0 raster index"""
    # ulx, xres, xskew, uly, yskew, yres
    xp = ul_x + (row * xres)
    yp = ul_y + (col * yres)
    return xp, yp


def get_xy(pt):
    return pt.x, pt.y


def get_distance(df):
    df["min_dist"] = df.geometry.distance(gpd.GeoSeries(df.point))
    return df


def parallelize_dataframe(df, func, n_cores=6):  # currently not used here
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


# read nadir file
print("Assuming a generic nadir file including columns names X,Y and ID ")
temp = pd.read_csv(nadir, sep=',')
geometry = [Point(xy) for xy in zip(temp['X'], temp['Y'])]
df_lines = gpd.GeoDataFrame(temp, geometry=geometry)
df_lines = df_lines.groupby(['ID'])['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else x.tolist())

print("Open tif")
ds = gdal.Open(raster)  # open tif
band = ds.GetRasterBand(band_number)
ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
max_width, max_height = ds.RasterXSize, ds.RasterYSize

print("Convert tif to array")
grey_array = band.ReadAsArray()

print("Get coordinates for each pixel")
pixel_coordinates_x = np.empty((int(max_height / downscale_factor), int(max_width / downscale_factor)))
pixel_coordinates_y = np.empty((int(max_height / downscale_factor), int(max_width / downscale_factor)))

print("Calculating coordinates for every pixel")
tmp = fast_coord.pixel_coord_fast(xres * downscale_factor, yres * downscale_factor, ulx, uly, pixel_coordinates_x,
                                  pixel_coordinates_y)

# This results in a 2d-array with x coordinates in column 1 and y coordinates in column 0
pixel_coordinates = np.asarray(tmp).swapaxes(0, 2)
pixel_coordinates = np.dstack([pixel_coordinates[:, :, 0].flatten(), pixel_coordinates[:, :, 1].flatten()]).squeeze()
# Make GeoDataFrame from the pixel coordinates
gpd_pixel_coordinates = gpd.GeoSeries([Point(row[1], row[0]) for row in tqdm(pixel_coordinates)])

print("Create offset around pixels to search for lines")
bbox = gpd_pixel_coordinates.bounds + [-offset, -offset, offset, offset]

print("Get Corresponding Nadir Lines")
hits = bbox.progress_apply(lambda row: list(df_lines.sindex.intersection(row)), axis=1)  # which nadir lines to consider
# Setup temporary dataframe
tmp = pd.DataFrame({
    # index of points (pixel of subimage) table
    "pt_idx": np.repeat(hits.index, hits.apply(len)),
    # ordinal position of nadir line  - access via iloc later
    "line_i": np.concatenate(hits.values)
})

print("Join points back to line")
tmp = tmp.join(df_lines.reset_index(drop=True), on="line_i")
tmp = tmp.join(gpd_pixel_coordinates.geometry.rename("point"), on="pt_idx")
tmp = gpd.GeoDataFrame(tmp, geometry="geometry", crs=gpd_pixel_coordinates.crs)

print("Calculate min_dist.")
# tmp = parallelize_dataframe(tmp, get_distance)  #this worked but is now crashing. leave it in for future though.
tmp = get_distance(tmp)  # the non-parallel execution

print("Sorting Values")
tmp = tmp.sort_values(['pt_idx', 'min_dist'], ascending=[True, True]).drop_duplicates('pt_idx').sort_index()
tmp['normalized_dist'] = (tmp['min_dist'] - tmp['min_dist'].min()) / (
        120 - tmp['min_dist'].min()) * 255

# Gridding and exporting
xypoints = tmp['point'].centroid
centroidlist = map(get_xy, xypoints)
X, Y = [list(t) for t in zip(*map(get_xy, xypoints))]
out = pd.DataFrame({
    "X": X,
    "Y": Y,
    "min_dist": tmp["min_dist"],
    "norm_dist": tmp['normalized_dist']
})

if export_csv_with_raw_data == 1:
    print("Export data to csv")
    out.to_csv(nadir + "_distance.csv", index=False)
else:
    print("No export selected")
    pass

# Use pygmt for gridding
x_min = ulx
x_max = ulx + max_width * xres
y_min = uly + max_height * yres
y_max = uly
region = str(str(x_min) + "/" + str(x_max) + '/' + str(y_min) + "/" + str(y_max) + "+ue")
if grid_input == 0:
    print("Gridding minimum distance values")
    surface = surface(x=X, y=Y, z=tmp["min_dist"], region=region, outfile=raster + "_min_dist.nc", spacing="0.25+e")
elif grid_input == 1:
    print("Gridding minimum distance values scaled to 0-255")
    surface = surface(x=X, y=Y, z=tmp['normalized_dist'], region=region, outfile=raster + '_min_dist_scaled.nc',
                      spacing="0.25+e")
else:
    print("No gridding was selected")
