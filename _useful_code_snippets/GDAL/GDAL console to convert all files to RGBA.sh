#batchfile neds to %%
# should give all subdirs

for /R %f in (.\*.tif) do @echo %f 

# translate all files to rgba in d:\converted folder
#in folder
for /f "delims=" %f in ('dir *.tif /b') do gdal_translate -of GTiff -ot Float32 -outsize 50% 50% -expand rgba -co COMPRESS=DEFLATE -co PREDICTOR=1 -co ZLEVEL=6 %f D:\converted\%f
#recursively
for /r %i in (*.tif) do gdal_translate -of GTiff -ot Float32 -outsize 100% 100% -expand rgba -co COMPRESS=DEFLATE -co PREDICTOR=1 -co ZLEVEL=6 %~pnxi  D:\convert\%~nxi