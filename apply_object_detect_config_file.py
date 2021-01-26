import os

#main1
#image_folder = '/media/peter/Daten_1/BalticSeaTraining/tifs/tiles/'
#image_type = '.tif'

#all
output = './output/AdlerGrund_Test1.csv'
labels_to_names = {0: 'stone'}
model_path = os.path.join('./resnet50_csv_SR100_17_r09.h5')
convert_model = 'yes'
detection_threshold = 0.2  #include detections with accuracy above
min_side=800
boundary_threshold = 0.4  #Stones smaller together will be merged
