# !!Double quotes "   "

for /r %i in (*.tif) do gdalwarp -s_srs "EPSG:32632" -t_srs "+proj=longlat +datum=WGS84 +no_defs" %~pnxi  %~nxi.utm.tif