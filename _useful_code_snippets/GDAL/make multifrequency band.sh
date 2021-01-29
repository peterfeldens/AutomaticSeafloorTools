Using 

gdalbuildvrt -separate RGB.vrt red.tif green.tif blue.tif

gdal_translate RGB.vrt RGB.tif


oder

gdal_merge.py [-o out_filename] [-of out_format] [-co NAME=VALUE]*
              [-ps pixelsize_x pixelsize_y] [-tap] [-separate] [-q] [-v] [-pct]
              [-ul_lr ulx uly lrx lry] [-init "value [value...]"]
              [-n nodata_value] [-a_nodata output_nodata_value]
              [-ot datatype] [-createonly] input_files

              e.g.
              gdal_merge.py -o steintest_multiband.tif -separate steintest.tif steintest_dist.tif steintest.tif
