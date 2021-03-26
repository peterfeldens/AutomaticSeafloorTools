# This reproduces the training dataset
mkdir /Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth
mkdir /Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth
mkdir /Users/peter/EXPERIMENT/current_run
mkdir /Users/peter/EXPERIMENT/temp


#Note mbes 64 pixel bs only and slope only

#cut
python cut_image_to_tiles.py \
/Users/peter/EXPERIMENT/datasets_objects/training/mosaics/mbes/depth \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth \
64 \
tif  \
--overlap=4


#split
python create_random_distribution.py \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth \
0.10 \
tif

#upscale


#relate with stone detection
python relate_database_and_images.py \
--image_directory=/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth/ \
--wildcards=tif \
--database_directory=/Users/peter/EXPERIMENT/datasets_objects/training/annotations \
--input_databases=mbes_ground.sqlite \
--input_classes=stone \
--out_directory=/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth/ \
--format=yolo

#python relate_database_and_images.py \
--image_directory=/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth/ \
--wildcards=tif \
--database_directory=/Users/peter/EXPERIMENT/datasets_objects/training/annotations \
--input_databases=mbes_ground.sqlite \
--input_classes=stone \
--out_directory=/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth/  \
--format=yolo


#add empty examples
#This is a bit hacky
#python relate_database_and_images.py \
--image_directory=/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth/ \
--wildcards=tif \
--database_directory=/Users/peter/EXPERIMENT/datasets_objects/training/annotations \
--input_databases=mbes_empty.sqlite    \
--input_classes=empty \
--out_directory=/Users/peter/EXPERIMENT/temp/ \
--format=yolo \
--empty_examples=1

for file in /Users/peter/EXPERIMENT/temp/*.txt; do
  rm $file
  touch $file
done
mv /Users/peter/EXPERIMENT/temp/*.txt /Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth/


python relate_database_and_images.py \
--image_directory=/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth/ \
--wildcards=tif \
--database_directory=/Users/peter/EXPERIMENT/datasets_objects/training/annotations \
--input_databases=mbes_empty.sqlite    \
--input_classes=empty \
--out_directory=/Users/peter/EXPERIMENT/temp/ \
--format=yolo \
--empty_examples=1

for file in /Users/peter/EXPERIMENT/temp/*.txt; do
  rm $file
  touch $file
done
mv /Users/peter/EXPERIMENT/temp/*.txt /Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth/



#Delete images with no labels (empty examples must be added separately)
python yolo_delete_images_with_no_label.py /Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth .tif

python yolo_delete_images_with_no_label.py \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth \
.tif


### Convert to greyscale
#no longer done..we make sure the input mosaics are correctlz saved
#convert if needed
python convert_to_greyscale.py \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth \
tif

#convert if needed
python convert_to_greyscale.py \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth \
tif

#convert
python convert_to_png.py \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth

rm /Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth/*.tif

python convert_to_png.py \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth

rm /Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth/*.tif


#sleep 1
#rotate
python yolo_rotate_img_and_boundaries.py \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth \
.png

python yolo_rotate_img_and_boundaries.py \
/Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth \
.png


#touch /Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth/classes.txt
#echo "stones" >> /Users/peter/EXPERIMENT/MBES_yolo64_pixtest_depth/classes.txt

#touch /Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth/classes.txt
#echo "stones" >> /Users/peter/EXPERIMENT/MBES_yolo64_pixtrain_depth/classes.txt


# continue with yolo_raun_training
