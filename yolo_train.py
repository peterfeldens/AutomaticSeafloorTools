import time # Required Arguments
import argparse
import os
import sys
parser = argparse.ArgumentParser()
parser.add_argument('--directory', type=str, help="BaseFolder")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

args.directory.strip("/")

os.chdir(args.directory)

cmd = 'rm /home/peter/images/*'
os.system(cmd)
cmd = 'rm /home/peter/images/train/*'
os.system(cmd)
cmd = 'rm /home/peter/images/test/*'
os.system(cmd)

cmd = 'git clone https://github.com/peterfeldens/AutomaticSeafloorTools.git'
os.system(cmd)

cmd = 'python /home/AutomaticSeafloorTools/cut_image_to_tiles.py \
/mnt/h/ki/datasets_objects/training/mosaics/sb \
/home/peter/images/train \
 512 \
tif \
--overlap 6'
os.system(cmd)

greyscale = True  #switch between greyscale or multiband training with additional image channels
if greyscale == True:
    cmd = 'python /home/peter/AutomaticSeafloorTools/convert_to_greyscale.py \
     /home/peter/images/train \
     /home/peter/images/train \
         .tif \
     --overwrite'
    os.system(cmd)

# Make test_train split of images
cmd = 'python /home/peter/AutomaticSeafloorTools/create_random_distribution.py \
 /home/peter/images/train \
 /home/peter/images/test \
    0.15 \
    tif'
os.system(cmd)


# Relate points and training database. Yolo option supports only 1 class at the moment
cmd = 'python /home/peter/AutomaticSeafloorTools/relate_database_and_images.py \
--image_directory=/home/peter/images/train \
--wildcards=tif \
--database_directory=/mnt/h/ki/datasets_objects/training/annotations \
--input_databases=v3pickedstone_utm.sqlite \
--input_classes=stone \
--out_directory=/home/peter/images/train \
--format=yolo '
os.system(cmd)

cmd = 'python /home/peter/AutomaticSeafloorTools/relate_database_and_images.py \
 --image_directory=/home/peter/images/test \
--wildcards=tif \
-database_directory=/mnt/h/ki/datasets_objects/training/annotations \
--input_databases=v3pickedstone_utm.sqlite \
--input_classes=stone \
 --out_directory=/home/peter/images/test \
--format=yolo '
os.system(cmd)

cmd = 'realpath /home/peter/images/train/*.txt > /home/peter/current_run/train.txt'
os.system(cmd)
cmd = 'realpath /home/peter/images/test/*.txt > /home/peter/current_run/test.txt'
os.system(cmd)

#Change .txt with .jpg
cmd = 'sed -i \'s/txt/jpg/g\' /home/peter/current_run/train.txt'
os.system(cmd)
cmd = 'sed -i \'s/txt/jpg/g\' /home/peter/current_run/train.txt'
os.system(cmd)


cmd = 'rm /home/peter/current_run/obj.names'
os.system(cmd)
cmd = 'rm /home/peter/current_run/obj.data'
os.system(cmd)
cmd = 'touch /home/peter/current_run/obj.names'
os.system(cmd)
cmd = 'echo "stones" >> /home/peter/current_run/obj.names'
os.system(cmd)

cmd = 'touch /home/peter/current_run/obj.data'
os.system(cmd)
cmd = 'echo "classes = 1" >> /home/peter/current_run/obj.data'
os.system(cmd)
cmd = 'echo "train = /home/peter/current_run/train.txt" >> /home/peter/current_run/obj.data'
os.system(cmd)
cmd = 'echo "valid = /home/peter/current_run/test.txt" >> /home/peter/current_run/obj.data'
os.system(cmd)
cmd = 'echo "names = /home/peter/current_run/obj.names" >> /home/peter/current_run/obj.data'
os.system(cmd)
cmd = 'echo "backup = /home/peter/current_run" >> /home/peter/current_run/obj.data'
os.system(cmd)


cmd = '/home/peter/darknet/darknet \
detector calc_anchors \
/home/peter/current_run/obj.data \
-num_of_clusters 9 \
-width 512 \
-height 512 \
-show'
os.system(cmd)

cmd = '/home/peter/darknet/darknet \
detector train \
/home/peter/current_run/obj.data \
/home/peter/current_run/yolov4_tiny.cfg \
/home/peter/Models/Yolo4/yolov4.conv.137 \
-map -dont_show'
os.system(cmd)


timestr = time.strftime("%Y%m%d-%H%M%S")
os.mkdir(timestr)

cmd = 'mv /home/peter/current_run/* /home/peter/'+timestr
os.system(cmd)



