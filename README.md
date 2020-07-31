Tools to make the 

https://github.com/fizyr/keras-retinanet

and

https://github.com/brade31919/SRGAN-tensorflow 

Working archives of these projects are stored in the dropbox. 


Manual for Retina-Net

Application of Retina Net to detect boulders in backscatter mosaics.

1. Install keras retina net from https://github.com/fizyr/keras-retinanet

TRAINING
2. Get training data:  Pick boundary boxes of boulders (and optionally negative examples) from backatter mosaics using QGIS. Examples are stored in Dropbox. The bounding boxes have to be exported as sqlite databases with the coordinates written in WKT format. Coordinates of mosaics and database should be UTM.
3. Create small tiles (25m² used in the paper) by using cutout_of_training_daty.py. This program can cut large mosaics in small tiles with overlap.
4. Relate database and tiles: Also in cutout_pf_training_data.py there is an option to generate vsv files from the sqlite database exported from Qgis. 
   The program can also buffer points, if only point data exists. It also adds a class name and splits the results in an training and validation .csv file.
5. The preocess has to be repeated for each picked class. Negatve examples need to be manaully copied to the training csv, eith no class given! This is a bit cumbersome. (see ./Annotations for examples)

5b: Optional: Use https://github.com/martinzlocha/anchor-optimization to optimize the anchor configuration in retina-nets config file

6. Run the model following the Readme of keras retina-net. Weights are stored in dropbox
 

7.(e.g. retinanet-train --backbone=resnet50 --weights=resnet50_coco_best_v2.1.0.h5 --epochs=50 --image-min-side=600 --snapshot-path=./snapshots csv  --val-annotations=./training_data/v2_15m_test.csv ./training_data/v2_15m_train.csv classes.csv
))
6a. You can use tensorboard to monitor the progress in the browser


USING the MODEL:

7. Once you have trained h5 model file, you can use the programm apply_model.py to use it to your data (needs to be tiled). 
   Specify the folder with image tiles, their size and the model path. The programm will output a csv with the detected boulder positions and their score. 
This can be loaded in QGIS. 

ANALYSIS:
Some further analysis options are given in Ausertung.ipynb.