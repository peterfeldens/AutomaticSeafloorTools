def getfiles(id='', pfad='.'):
    import os
    # Gibt eine Liste mit Dateien in PFAD und der Endung IDENTIFIER aus.
    files = []
    for file in os.listdir(pfad):
        if file.endswith(id):
            files.append(str(file))
    return files


def parse_args(parser):
    try:
        args = parser.parse_args()
    except Exception as ex:
        parser.print_help()
        print(ex)
    return args



# Image Processing

def get_boundaries(image):
    '''
    Bestimmen der Bildgrenzen
    '''
    src = gdal.Open(image)
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    return ulx, xres, uly, yres, lrx, lry


def convert_pixel_to_real(image, box):
    # box : A list of 4 elements (x1, y1, x2, y2).
    ulx, xres, uly, yres, lrx, lry = get_boundaries(image)
    box_ulx = box[0]
    box_uly = box[1]
    box_lrx = box[2]
    box_lry = box[3]

    assert yres < 0   #otherwise, upper left is not the origin of the image

    # Convert pixel to real
    box_ulx_coord = ulx + (box_ulx * xres)
    box_uly_coord = uly + (box_uly * yres) #yres ist negativv
    box_lrx_coord = ulx + (box_lrx * xres)
    box_lry_coord = uly + (box_lry * yres)
    box_mean_x = (box_ulx_coord + box_lrx_coord) /2
    box_mean_y = (box_uly_coord + box_lry_coord) /2
    return box_ulx_coord, box_uly_coord, box_lrx_coord, box_lry_coord, box_mean_x, box_mean_y