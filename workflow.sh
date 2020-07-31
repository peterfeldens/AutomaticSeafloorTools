#Prepare tiles and downsample. Needs conda activate GIS at the moment

FAKTOR=2
IMAGESIZE=100
THRESHOLD=200




python cut_image_to_tiles.py /Volumes/Work/ /Volumes/Work/tiles/ $IMAGESIZE .tif

python convert_to_png.py /Volumes/Work/tiles

#python delete_only_white_images.py /home/peter/training/north_sea_training/tiles .png $THRESHOLD
#python check_for_correct_size.py /home/peter/training/north_sea_training/tiles $IMAGESIZE .png



#mkdir /Volumes/Work/valid_100_pixels_LRx2/
#mkdir /Volumes/Work/valid_100_pixels_HR
#mkdir /home/peter/training/north_sea_training/tiles/train/HR/
#mkdir /home/peter/training/north_sea_training/tiles/train/LR/

#mkdir /home/peter/training/north_sea_training/tiles/valid/
#mkdir /home/peter/training/north_sea_training/tiles/valid/HR
#mkdir /home/peter/training/north_sea_training/tiles/valid/LR

#mkdir /home/peter/training/north_sea_training/tiles/original_tif

#echo "Move files"

find /Volumes/Work/tiles -name '*.png' -exec mv "{}" /Volumes/Work/valid_100_pixels_HR \;
#find /home/peter/training/north_sea_training/tiles -name '*.tif' -exec mv "{}" /home/peter/training/north_sea_training/tifs/tiles \;

#echo "Create Random distribution"

#python create_random_distribution.py /home/peter/training/north_sea_training/tiles/train/HR /home/peter/training/north_sea_training/tiles/valid/HR 0.10 .png

#echo "Downsample images"

python downsample_image.py /Volumes/Work/valid_100_pixels_HR /Volumes/Work/valid_100_pixels_LRx2 $FAKTOR .png

#python downsample_image.py /home/peter/training/north_sea_training/tiles/valid/HR /home/peter/training/north_sea_training/tiles/valid/LR $FAKTOR .png

# Make fake RGBs of everything to get it into Neuralnetwork
python convert_to_rgb.py /Volumes/Work/valid_100_pixels_LRx2 /Volumes/Work/valid_100_pixels_LRx2 .png 

#python convert_to_rgb.py /home/peter/training/north_sea_training/tiles/train/HR /home/peter/training/north_sea_training/tiles/train/HR .png 

#python convert_to_rgb.py /home/peter/training/north_sea_training/tiles/valid/LR /home/peter/training/north_sea_training/tiles/valid/LR .png 

#python convert_to_rgb.py /home/peter/training/north_sea_training/tiles/valid/HR /home/peter/training/north_sea_training/tiles/valid/HR .png 


