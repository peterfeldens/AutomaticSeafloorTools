def create_vrt(image_type, in_path, outname = 'vrt_of_file.vrt'):
    import os, gdal, sys
    sys.path.append('/home/peter/BSSC/Skripte')
    import FUNCTIONS_FILE_SYSTEM as ffs
    #%% Combine all files in the folder in a virtual GeoTif
    # Get a file list of all png files. Write it to a textfile to feed into gdal
    # for the creation of the virtual tif
    file_list = ffs.getfiles(image_type, in_path)
    print file_list
    with open(in_path + 'liste.txt', 'w') as thefile:
        for item in file_list:
            print>>thefile, item
    # The virtual GeoTif File is calles vrt_of_files.vrt
    os.chdir(in_path)
    com_string = "gdalbuildvrt -addalpha  -srcnodata '255 255 255' -input_file_list liste.txt vrt_of_files.vrt"
    print com_string
    os.system(com_string)
    return

def delete_black_white(path, ID):
    import os, sys
    from scipy.misc import imread
    import numpy as np
    sys.path.append('/home/peter/BSSC/Skripte')
    import FUNCTIONS_FILE_SYSTEM as ffs
    # Delete images that only have white or black colors
    training_files = ffs.getfiles(ID,path)
    for file in training_files:
        print file
        image = imread(path + file, flatten = True)
        values = np.unique(image)
        if list(values) and all((elem == 255) or (elem == 0) for elem in list(values)):
            print("Only black and white")
            os.remove(path + file)
            if ID == 'png':
                os.remove(path + file + '.aux.xml')
    return
    
    
    def create_vrt(image_type, in_path, outname = 'vrt_of_file.vrt'):
    """
    Create a virtual geotif from image files wihtin a folder

    only runs in the osgeo shell at the moment
    """
    import os, gdal, sys
    sys.path.append('F:/GoogleDrive/dev/Functions')
    sys.path.append('/home/peter/gdrive/dev/Functions')
    import FUNCTIONS_FILE_SYSTEM as ffs
    #%% Combine all files in the folder in a virtual GeoTif
    # Get a file list of all png files. Write it to a textfile to feed into gdal
    # for the creation of the virtual tif
    file_list = ffs.getfiles(image_type, in_path)
    print(file_list)
    with open(in_path + 'liste.txt', 'w') as thefile:
        for item in file_list:
            print>>thefile, item
    # The virtual GeoTif File is calles vrt_of_files.vrt
    os.chdir(in_path)
    com_string = "gdalbuildvrt -addalpha  -srcnodata '255 255 255' -input_file_list liste.txt vrt_of_files.vrt"
    print(com_string)
    os.system(com_string)
    return

def extract_subimages_by_coordinates():
    print("Function extract_subimages not yet implemented")
    return

def split_images_regular_blocks(infile, out_path, out_filename, tile_size_x = 25, tile_size_y = 25, out_format = 'PNG'):
    """
    Split images into blocks
    Purpose is feeding them into a neural network predict_generatorself.

    The input file must be VRT

    Image Resolution and projection are the same as the input data, could be
    changed here easily though if the need arised by adjusting xres and yres

    we try to use a gdal python binding implemenation

    projWin could be used instead of SrcWin to extract subpixels, see
    http://gdal.org/python/
    """
    from osgeo import gdal

    #Import vrt
    #Open existing dataset and get numbers of pixels and resolution
    src = gdal.Open(infile)
    xsize = src.RasterXSize
    ysize = src.RasterYSize
    geotransform = src.GetGeoTransform()
    xres = geotransform[1]
    yres = geotransform[5]

    #Open output format driver, see gdal_translate --formats for list
    #format = out_format
    #driver = gdal.GetDriverByName( format )

    # Create tiles
    for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
            out = str(out_path) + str(out_filename) + str(i) + "_" + str(j) + '.' + str(out_format)
            ds = gdal.Translate(
                    out, src, xRes=xres, yRes=yres,
                    srcWin = [i, j, tile_size_x, tile_size_y]
                    )
            ds = None
    return

def get_coordinates_from_images(in_folder, img_type = 'TIF'):
    '''
    Read a number of image files from a folder. if present,
    gdal is used to extracxt the cornder coordinates of the image
    and the x and y resolution
    
    Returns a pandas dataframe with coordinates and image resolutions
    '''
    
    from osgeo import gdal
    import os
    import pandas as pd
    
    coordinate_liste = []
    for i in os.listdir(in_folder):
        if i.endswith(img_type):
            #print(i)
            ds = gdal.Open(in_folder + i)
           # print("Driver: {}/{}".format(ds.GetDriver().ShortName,
           #                  ds.GetDriver().LongName))
            ulx, xres, xskew, uly, yskew, yres  = ds.GetGeoTransform()
            lrx = ulx + (ds.RasterXSize * xres)
            lry = uly + (ds.RasterYSize * yres)
            middle_y = (lry + uly) / 2
            middle_x = (lrx + ulx) / 2
            coordinate_liste.append([middle_x, middle_y, ulx, uly, lrx, lry, xres, yres])

    df = pd.DataFrame(coordinate_liste)
    df.columns = ['middle_x', 'middle_y','ulx','uly', 'lrx', 'lry', 'xres', 'yres']
    return df

def get_coordinates_from_image(infile, img_type = 'TIF'):
    '''
    Get coordinates from a single image
    gdal is used to extracxt the cornder coordinates of the image
    and the x and y resolution
    '''
    
    from osgeo import gdal
    ds = gdal.Open(infile)
    ulx, xres, xskew, uly, yskew, yres  = ds.GetGeoTransform()
    lrx = ulx + (ds.RasterXSize * xres)
    lry = uly + (ds.RasterYSize * yres)

    return ulx,uly, lrx, lry, xres, yres


def delete_black_white(path, ID):
    """
    Delete all images in a folder that contain only black or white values
    """
    import os, sys
    from scipy.misc import imread
    import numpy as np
    sys.path.append('F:/GoogleDrive/dev/Functions')
    import FUNCTIONS_FILE_SYSTEM as ffs
    # Delete images that only have white or black colors
    training_files = ffs.getfiles(ID,path)
    for file in training_files:
        if os.path.isfile(file):
            print(file)
            image = imread(path + file, flatten = True)
            values = np.unique(image)
            if list(values) and all((elem == 255) or (elem == 0) or (elem == 'NaN') for elem in list(values)):
                print("Only black and white")
                os.remove(path + file)
                if ID == 'png':
                    os.remove(path + file + '.aux.xml')
    return

def reduce_number_grayscales(path, ID, greylevel):
    """
    Reduce the number of greyscales within an image
    """
    import os, sys
    from scipy.misc import imread
    from scipy.misc import imsave
    sys.path.append('F:/GoogleDrive/dev/Functions')
    import FUNCTIONS_FILE_SYSTEM as ffs
    import FUNCTIONS_ARRAYS as ffa
    # Ream Images, reduce number of greyelvels, save back
    training_files = ffs.getfiles(ID,path)
    for img in training_files:
        # get basenames
        base = os.path.splitext(img)[0]
        outfile = path + base + '.' + ID
        #read image
        image = imread(path + img, flatten = True)
        #reduce number of greyscales
        image_red = ffa.image_stretch(image, greylevel)
        #save image under new name
        imsave(outfile, image_red)
    return

def azimuthalAverage(image, center=None):
    """
    Calculate the azimuthally averaged radial profile.

    image - The 2D image
    center - The [x,y] pixel coordinates used as the center. The default is
             None, which then uses the center of the image (including
             fracitonal pixels).

    """
    import numpy as np
    # Calculate the indices from the image
    y, x = np.indices(image.shape)

    if not center:
        center = np.array([(x.max()-x.min())/2.0, (x.max()-x.min())/2.0])

    r = np.hypot(x - center[0], y - center[1])

    # Get sorted radii
    ind = np.argsort(r.flat)
    r_sorted = r.flat[ind]
    i_sorted = image.flat[ind]

    # Get the integer part of the radii (bin size = 1)
    r_int = r_sorted.astype(int)

    # Find all pixels that fall within each radial bin.
    deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
    rind = np.where(deltar)[0]       # location of changed radius
    nr = rind[1:] - rind[:-1]        # number of radius bin

    # Cumulative sum to figure out sums for each radius bin
    csim = np.cumsum(i_sorted, dtype=float)
    tbin = csim[rind[1:]] - csim[rind[:-1]]

    radial_prof = tbin / nr

    return radial_prof

def radial_data(data,annulus_width=1,working_mask=None,x=None,y=None,rmax=None):
    """
    r = radial_data(data,annulus_width,working_mask,x,y)

    A function to reduce an image to a radial cross-section.

    INPUT:
    ------
    data   - whatever data you are radially averaging.  Data is
            binned into a series of annuli of width 'annulus_width'
            pixels.
    annulus_width - width of each annulus.  Default is 1.
    working_mask - array of same size as 'data', with zeros at
                      whichever 'data' points you don't want included
                      in the radial data computations.
      x,y - coordinate system in which the data exists (used to set
             the center of the data).  By default, these are set to
             integer meshgrids
      rmax -- maximum radial value over which to compute statistics

     OUTPUT:
     -------
      r - a data structure containing the following
                   statistics, computed across each annulus:
          .r      - the radial coordinate used (outer edge of annulus)
          .mean   - mean of the data in the annulus
          .std    - standard deviation of the data in the annulus
          .median - median value in the annulus
          .max    - maximum value in the annulus
          .min    - minimum value in the annulus
          .numel  - number of elements in the annulus
    """

# 2010-03-10 19:22 IJC: Ported to python from Matlab
# 2005/12/19 Added 'working_region' option (IJC)
# 2005/12/15 Switched order of outputs (IJC)
# 2005/12/12 IJC: Removed decifact, changed name, wrote comments.
# 2005/11/04 by Ian Crossfield at the Jet Propulsion Laboratory

    import numpy as np

    class radialDat:
        """Empty object container.
        """
        def __init__(self):
            self.mean = None
            self.std = None
            self.median = None
            self.numel = None
            self.max = None
            self.min = None
            self.r = None

    #---------------------
    # Set up input parameters
    #---------------------
    data = np.array(data)

    if working_mask==None:
        working_mask = np.ones(data.shape,bool)

    npix, npiy = data.shape
    if x==None or y==None:
        x1 = np.arange(-npix/2.,npix/2.)
        y1 = np.arange(-npiy/2.,npiy/2.)
        x,y = np.meshgrid(y1,x1)

    r = abs(x+1j*y)

    if rmax==None:
        rmax = r[working_mask].max()

    #---------------------
    # Prepare the data container
    #---------------------
    dr = np.abs([x[0,0] - x[0,1]]) * annulus_width
    radial = np.arange(rmax/dr)*dr + dr/2.
    nrad = len(radial)
    radialdata = radialDat()
    radialdata.mean = np.zeros(nrad)
    radialdata.std = np.zeros(nrad)
    radialdata.median = np.zeros(nrad)
    radialdata.numel = np.zeros(nrad)
    radialdata.max = np.zeros(nrad)
    radialdata.min = np.zeros(nrad)
    radialdata.r = radial

    #---------------------
    # Loop through the bins
    #---------------------
    for irad in range(nrad): #= 1:numel(radial)
      minrad = irad*dr
      maxrad = minrad + dr
      thisindex = (r>=minrad) * (r<maxrad) * working_mask
      if not thisindex.ravel().any():
        radialdata.mean[irad] = np.nan
        radialdata.std[irad]  = np.nan
        radialdata.median[irad] = np.nan
        radialdata.numel[irad] = np.nan
        radialdata.max[irad] = np.nan
        radialdata.min[irad] = np.nan
      else:
        radialdata.mean[irad] = data[thisindex].mean()
        radialdata.std[irad]  = data[thisindex].std()
        radialdata.median[irad] = np.median(data[thisindex])
        radialdata.numel[irad] = data[thisindex].size
        radialdata.max[irad] = data[thisindex].max()
        radialdata.min[irad] = data[thisindex].min()

    #---------------------
    # Return with data
    #---------------------

    return radialdata

def decompose_mosaic(IN_FILE, OUT_FOLDER, BLOCK_SIZE, label = 0, FLATTEN = True, filewrite = 'no', transpose = 'no'):
    """
    Created on Wed Nov  1 13:40:57 2017

    To develop function that combine images into mosaics and can also decompose them

    At the moment, we only work on greyscale images - not tested on multifreq-data;
    the blockview function will only work on 2d matrcies.

    Probably, all chanells of an RGB image will have to be split seperately

    @author: peter
    """
    #decompose image mosaic into a series of png images
    from scipy.misc import imread
    from scipy.misc import imsave
    import sys
    sys.path.append('F:/GoogleDrive/dev/Functions')
    import FUNCTIONS_ARRAYS as ffa
    #1. Rad image as matrix
    img = imread(IN_FILE, flatten = FLATTEN)
    if transpose == 'yes':
        img = img.transpose()

    #2. Read 20x20 blocks
    blockviews = ffa.block_view(img, block = (BLOCK_SIZE, BLOCK_SIZE))
    #3 try to infer numbers for spliiting of labels
    #3. Make list of images (i.e. remove one dimension)
    blockviews = blockviews.reshape(-1, BLOCK_SIZE, BLOCK_SIZE)
    #4. Make Labelz


    if filewrite == 'yes':
        for i in range(blockviews.shape[0]):
            out_name = str(OUT_FOLDER) + str(label) + '_' + str(i) + '.png'
            out_image = blockviews[i,:,:]
            imsave(out_name, out_image)
    return blockviews, label

def export_image_as_pckl(path,image, flatten = True):
    from scipy.misc import imread
    data = imread(path+image, flatten = flatten)
