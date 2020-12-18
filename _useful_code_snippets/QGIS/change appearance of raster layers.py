change_appearance_of_raster_layers.py


#Workflow correction of Geo-Data

# Convert paletted files in qgis
layers = qgis.utils.iface.legendInterface().layers()
for layer in layers:
	layer.setDrawingStyle('PalettedColor')
	layer.renderer().setAlphaBand(2)
	layer.triggerRepaint()

#