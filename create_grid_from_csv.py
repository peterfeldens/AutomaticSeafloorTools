filtered_grid = 'no'  # create a second grid file with gaussian filter
#merge csv files and make large grid
# gridding

region = str(str(x_min) + "/" + str(x_max) + '/' + str(y_min) + "/" + str(y_max))
x_min = int(np.floor(glcm_dataframe.X.min()))
x_max = int(np.ceil(glcm_dataframe.X.max()))
y_min = int(np.floor(glcm_dataframe.Y.min()))
y_max = int(np.ceil(glcm_dataframe.Y.max()))
grid_out = str(file_out) + ".nc"
#command = "gmt surface " + file_out + " -I" + str(grid_res) + " -R" + region + " -G" + grid_out
#os.system(command)#
#
#if filtered_grid == 'yes':
#    filtered_grid_out = str(file_out) + "_smooth.nc"
#    command = "gmt grdfilter " + grid_out + " -D0 -Fg2 " + " -G" + filtered_grid_out
#    os.system(command)