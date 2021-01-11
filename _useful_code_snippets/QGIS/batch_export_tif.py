from qgis.core import *

pathToFile = "/home/peter/Experiment/2020_12_22_classify_AdlerGrund/to_be_processed/"  #end with /
trs = QgsCoordinateReferenceSystem()
trs.createFromId(32633)
suffix = "_UTM33WGS84"
prefix = "BSH_"
layers = [layer for layer in QgsProject.instance().mapLayers().values()]

for layer in layers:
    extent = layer.extent()
    width, height = layer.width(), layer.height()
    pipe = QgsRasterPipe()
    provider = layer.dataProvider()
    pipe.set(provider.clone())


    newName = pathToFile + prefix + layer.name() + suffix + ".tif"

    file_writer = QgsRasterFileWriter(newName)

    file_writer.writeRaster(pipe,
                         width,
                         height,
                         extent,
                         trs)   #coord beibehalnte mit layer.crs
