# This reproduces the training dataset
mkdir /Users/peter/EXPERIMENT/SSS_yolo64_pixtrain_manual
mkdir /Users/peter/EXPERIMENT/SSS_yolo64_pixtest_manual
mkdir /Users/peter/EXPERIMENT/current_run
mkdir /Users/peter/EXPERIMENT/temp

#split
#python create_random_distribution.py \
#/Users/peter/EXPERIMENT/SSS_yolo64_pixtrain_manual \
#/Users/peter/EXPERIMENT/SSS_yolo64_pixtest_manual \
#0.10 \
#png \
#--txtfiles=1

#upscale

python yolo_rotate_img_and_boundaries.py \
/Users/peter/EXPERIMENT/SSS_yolo64_pixtest_manual \
.png

python yolo_rotate_img_and_boundaries.py \
/Users/peter/EXPERIMENT/SSS_yolo64_pixtrain_manual \
.png


#touch /Users/peter/EXPERIMENT/SSS_yolo64_pixtest_manual/classes.txt
#echo "stones" >> /Users/peter/EXPERIMENT/SSS_yolo64_pixtest_manual/classes.txt

#touch /Users/peter/EXPERIMENT/SSS_yolo64_pixtrain_manual/classes.txt
#echo "stones" >> /Users/peter/EXPERIMENT/SSS_yolo64_pixtrain_manual/classes.txt


# continue with yolo_raun_training
