# This reproduces the training dataset
mkdir /Users/peter/EXPERIMENT/MBES_yolo32_pixtrain
mkdir /Users/peter/EXPERIMENT/MBES_yolo32_pixtest
mkdir /Users/peter/EXPERIMENT/current_run
mkdir /Users/peter/EXPERIMENT/temp


#Note mbes 64 pixel bs only and slope only

#cut
python cut_image_to_tiles.py \
/Users/peter/TeamDropbox/Paper/DeepLearning/2021_multidimensional/data/Grids_Mosaics/mband \
/Users/peter/EXPERIMENT/MBES_yolo32_pixtrain \
32 \
tif  \
--overlap=4

#split
python create_random_distribution.py \
/Users/peter/EXPERIMENT/MBES_yolo32_pixtrain \
/Users/peter/EXPERIMENT/MBES_yolo32_pixtest \
0.15 \
tif

#upscale


#relate with stone detection
python relate_database_and_images.py \
--image_directory=/Users/peter/EXPERIMENT/MBES_yolo32_pixtrain/ \
--wildcards=tif \
--database_directory=/Users/peter/TeamDropbox/Paper/DeepLearning/2021_multidimensional/data/manual_picks \
--input_databases=mbes_ground.sqlite \
--input_classes=stone \
--out_directory=/Users/peter/EXPERIMENT/MBES_yolo32_pixtrain/ \
--format=yolo

python relate_database_and_images.py \
--image_directory=/Users/peter/EXPERIMENT/MBES_yolo32_pixtest/ \
--wildcards=tif \
--database_directory=/Users/peter/TeamDropbox/Paper/DeepLearning/2021_multidimensional/data/manual_picks \
--input_databases=mbes_ground.sqlite \
--input_classes=stone \
--out_directory=/Users/peter/EXPERIMENT/MBES_yolo32_pixtest/  \
--format=yolo


#add empty examples
#This is a bit hacky
python relate_database_and_images.py \
--image_directory=/Users/peter/EXPERIMENT/MBES_yolo32_pixtest/ \
--wildcards=tif \
--database_directory=/Users/peter/TeamDropbox/Paper/DeepLearning/2021_multidimensional/data/manual_picks \
--input_databases=mbes_empty.sqlite \
--input_classes=empty \
--out_directory=/Users/peter/EXPERIMENT/temp/ \
--format=yolo \
--empty_examples=1

for file in /Users/peter/EXPERIMENT/temp/*.txt; do
  rm $file
  touch $file
done
mv /Users/peter/EXPERIMENT/temp/*.txt /Users/peter/EXPERIMENT/MBES_yolo32_pixtest/


python relate_database_and_images.py \
--image_directory=/Users/peter/EXPERIMENT/MBES_yolo32_pixtrain/ \
--wildcards=tif \
--database_directory=/Users/peter/TeamDropbox/Paper/DeepLearning/2021_multidimensional/data/manual_picks \
--input_databases=mbes_empty.sqlite \
--input_classes=empty \
--out_directory=/Users/peter/EXPERIMENT/temp/ \
--format=yolo \
--empty_examples=1

for file in /Users/peter/EXPERIMENT/temp/*.txt; do
  rm $file
  touch $file
done
mv /Users/peter/EXPERIMENT/temp/*.txt /Users/peter/EXPERIMENT/MBES_yolo32_pixtrain/



#Delete images with no labels (empty examples must be added separately)
python yolo_delete_images_with_no_label.py /Users/peter/EXPERIMENT/MBES_yolo32_pixtrain .tif

python yolo_delete_images_with_no_label.py \
/Users/peter/EXPERIMENT/MBES_yolo32_pixtest \
.tif


### Convert to greyscale
#no longer done..we make sure the input mosaics are correctlz saved

#convert
python convert_to_png.py \
/Users/peter/EXPERIMENT/MBES_yolo32_pixtest

rm /Users/peter/EXPERIMENT/MBES_yolo32_pixtest/*.tif

python convert_to_png.py \
/Users/peter/EXPERIMENT/MBES_yolo32_pixtrain

rm /Users/peter/EXPERIMENT/MBES_yolo32_pixtrain/*.tif


sleep 1
#rotate
python yolo_rotate_img_and_boundaries.py \
/Users/peter/EXPERIMENT/MBES_yolo32_pixtest \
.png

python yolo_rotate_img_and_boundaries.py \
/Users/peter/EXPERIMENT/MBES_yolo32_pixtrain \
.png


#touch /Users/peter/EXPERIMENT/MBES_yolo32_pixtest/classes.txt
#echo "stones" >> /Users/peter/EXPERIMENT/MBES_yolo32_pixtest/classes.txt

#touch /Users/peter/EXPERIMENT/MBES_yolo32_pixtrain/classes.txt
#echo "stones" >> /Users/peter/EXPERIMENT/MBES_yolo32_pixtrain/classes.txt


# continue with yolo_raun_training
