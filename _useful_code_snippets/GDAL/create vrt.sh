#change into d:\converted directory
# Make sure there is no prvious merge tif file in da folder
dir /b *.tif > tiflist.txt
gdalbuildvrt -addalpha  -srcnodata "0 0 0" -input_file_list tiflist.txt vrt_of_files.vrt
#export as tif not needed if .vrt is tiled
gdal_translate vrt_of_files.vrt output.tiff