import os, gdal

in_path='D:/converted/'
input_filename='vrt_of_files.vrt'

out_path='D:/'
output_filename='tile_'

tile_size_x=12000
tile_size_y=12000

xres = 1
yres = 1

ds = gdal.Open(in_path + input_filename)
xsize = ds.RasterXSize
ysize = ds.RasterYSize




for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        com_string = "gdal_translate -of GTIFF -tr 1 1 -srcwin " + str(i)+ ", "   + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        os.system(com_string)