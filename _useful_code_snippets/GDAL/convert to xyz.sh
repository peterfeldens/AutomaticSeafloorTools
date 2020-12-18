# conver to xyz files
for /r %i in (*.utm.tif) do gdal_translate -of XYZ  %~pnxi  %~nxi.xyz