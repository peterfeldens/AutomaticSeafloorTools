FUNCTIONS_GLCM.py


################################################################################
###########T################################################
################################################################################
def greycomatrix(image, distances, angles=[0], levels=256, Symmetrie=1, Normiert=1):
	#Berechnen der Greycomatrix
	from skimage.feature import greycomatrix
	import numpy as np
	distances=np.reshape(distances,1)
	out=greycomatrix(image, distances, angles, levels, symmetric=Symmetrie, normed=Normiert)
	return out

def greycoparameters(glcm,angle, param):
    import numpy as np
#Calculation of the Parameters for the four angles
    result = []
    number_angles = len(angle)
    if param == 'ASM':
        for i in range(number_angles):
            ASM = []
            ASM.append(greycoprops(glcm[:,:,:,[i]],'ASM'))   #Für EINE Distanz!! und alle 4 Winkel
        result = np.sum(ASM)/number_angles

    elif param == 'ENTROPY':
        ENTROPY=[]
        for i in range(number_angles):
                ENTROPY.append(greycoprops(glcm[:,:,:,[i]],'entropy'))   #Für EINE Distanz!! und alle 4 Winkel
        result = np.sum(ENTROPY)/number_angles

    elif param == 'ENERGY':
        ENERGY = []
        for i in range(number_angles):
            ENERGY.append(greycoprops(glcm[:,:,:,[i]],'energy'))   #Für EINE Distanz!! und alle 4 Winkel
        result = np.sum(ENERGY)/number_angles

    elif param == 'CORRELATION':
        CORRELATION = []
        for i in range(number_angles):
            CORRELATION.append(greycoprops(glcm[:,:,:,[i]],'correlation'))   #Für EINE Distanz!! und alle 4 Winkel
        result = np.sum(CORRELATION)/number_angles

    elif param == 'CONTRAST':
        CONTRAST = []
        for i in range(number_angles):
            CONTRAST.append(greycoprops(glcm[:,:,:,[i]],'contrast'))   #Für EINE Distanz!! und alle 4 Winkel
        result=np.sum(CONTRAST)/number_angles

    elif param == 'DISSIMILARITY':
        DISSIMILARITY = []
        for i in range(number_angles):
            DISSIMILARITY.append(greycoprops(glcm[:,:,:,[i]],'dissimilarity'))   #Für EINE Distanz!! und alle 4 Winkel
        result = np.sum(DISSIMILARITY)/number_angles

    elif param == 'HOMOGENEITY':
        HOMOGENEITY = []
        for i in range(number_angles):
            HOMOGENEITY.append(greycoprops(glcm[:,:,:,[i]],'homogeneity'))   #Für EINE Distanz!! und alle 4 Winkel
        result=np.sum(HOMOGENEITY)/number_angles

    elif param == 'MAXPROB':
        MAXPROB = []
        for i in range(number_angles):
            MAXPROB.append(greycoprops(glcm[:,:,:,[i]],'maxprob'))   #Für EINE Distanz!! und alle 4 Winkel
        result=np.sum(MAXPROB)/number_angles

    elif param == 'GLCMMEAN':
        GLCMMEAN = []
        for i in range(number_angles):
            GLCMMEAN.append(greycoprops(glcm[:,:,:,[i]],'glcmmean'))   #Für EINE Distanz!! und alle 4 Winkel
        result=np.sum(GLCMMEAN)/number_angles

    else:
        print('Unknown Texture Parameter: ', param)

    return result

def greycoprops(P, prop):
	#Berechnen der Texturparameter
	import numpy as np

	assert P.ndim == 4
	(num_level, num_level2, num_dist, num_angle) = P.shape
	assert num_level == num_level2
	assert num_dist > 0
	assert num_angle > 0

	# create weights for specified property:
	#d.h. lege fest, wie stark die Einträge entfernt der Hauptdiagonale zählen.
	I, J = np.ogrid[0:num_level, 0:num_level] #Erzeugt eine Matrix mit den verwendeten Grauwerteinträgen
	if prop == 'contrast':
		weights = (I - J) ** 2  #Wenn I=J leigt die Zelle auf der Hauptdiagonalen, dh die nachbarn sind genau gleich -> Wert 0
	elif prop == 'dissimilarity':
		weights = np.abs(I - J)	#Hier steigen die Wichtungen von der Hauptdiagonalen nicht mehr exponentiell an
	elif prop == 'homogeneity':
		weights = 1/(1. + (I - J) ** 2)  #Hier wird die Hautdiagonale am stärksten gewichtet
	elif prop=='entropy':
		pass #Entropy does not need a weight
	elif prop in ['ASM', 'energy', 'correlation', 'maxprob', 'glcmmean']:
		pass # These values do not need weights
	else:
		raise ValueError('%s is an invalid property' % (prop))

		# compute property for each GLCM
	if prop == 'energy':
		results = []

		#Methode 1:
		#for i in range(num_level):
		#	for j in range(num_level):
		#		results.append(P[i][j]**2)
		#results = np.sum(results)
		#results = np.sqrt(results)

		#Methode 2:
		results = np.apply_over_axes(np.sum, (P**2), axes=(0, 1))[0, 0]
		results = np.sqrt(results)
	elif prop == 'ASM':
		results = []

		#Berechnugnsmethode 1:
		#for i in range(num_level):
		#	for j in range(num_level):
		#		results.append(P[i][j]**2)
		#results = np.sum(results)

		#Berechnungsmethode 2
		results = np.apply_over_axes(np.sum, (P**2), axes=(0, 1))[0, 0]
	elif prop=='entropy':
		results = []

		#Berechnungsmethode 1, funktioniert, ist verstänlich und langsam
		#for i in range(num_level):
		#	for j in range(num_level):
		#		results.append(P[i][j] * np.log(P[i][j]))
		#results = np.nan_to_num(results)
		#results = -np.sum(results)

		#Berechnungsmethode 2. Ist wesentlich schneller.
		def log0(x):
		#Wir müssen Log von 0 als 0 definieren sonst bricht das alles zusammen.
			return np.where(x==0., 0., -np.log(x))
		results = np.apply_over_axes(np.sum, (P * log0(P)), axes=(0, 1))[0, 0]

	elif prop == 'correlation':
		results = np.zeros((num_dist, num_angle), dtype=np.float64)
		I = np.array(range(num_level)).reshape((num_level, 1, 1, 1))
		J = np.array(range(num_level)).reshape((1, num_level, 1, 1))
		diff_i = I - np.apply_over_axes(np.sum, (I * P), axes=(0, 1))[0, 0]
		diff_j = J - np.apply_over_axes(np.sum, (J * P), axes=(0, 1))[0, 0]

		std_i = np.sqrt(np.apply_over_axes(np.sum, (P * (diff_i) ** 2), axes=(0, 1))[0, 0])
		std_j = np.sqrt(np.apply_over_axes(np.sum, (P * (diff_j) ** 2), axes=(0, 1))[0, 0])
		cov = np.apply_over_axes(np.sum, (P * (diff_i * diff_j)), axes=(0, 1))[0, 0]
		# handle the special case of standard deviations near zero
		mask_0 = std_i < 1e-15
		mask_0[std_j < 1e-15] = True
		results[mask_0] = 1

		# handle the standard case
		mask_1 = mask_0 == False
		results[mask_1] = cov[mask_1] / (std_i[mask_1] * std_j[mask_1])

	elif prop in ['contrast', 'dissimilarity', 'homogeneity']:
		results=[]
		weights = weights.reshape((num_level, num_level, 1, 1))
		results = np.apply_over_axes(np.sum, (P * weights), axes=(0, 1))[0, 0]

	elif prop == 'maxprob':
		results=[]
		results = P.max()

	elif prop == 'glcmmean':
		results=[]
		results = np.std(P)

	return results


def image_stretch(img,greylevels, v=1):
	#####NUR NOCH AUS KOMATIBILITÄTSGRÜNDEN HIER: AKTUELLE VERSION IN ARRAYS"
#Geht von einem 8bit Graustufenbild aus und reduziert es auf gewünschte Farbskala
#Das ist eigentlich noch ungenau, es müsste gerundet werden, und dann als Integer zurückgegeben

#factor=1./int(img.max())*(greylevels-1)
#a= img * factor
     greylevels = greylevels -1 #account for the 0
     img_min = 0
     img_max = greylevels
     img_std = (img -img_min) / (img_max - img_min)

     img_scaled = img_std * (greylevels - 0) + 0
     out=img_scaled.astype(int)

     if v==1:
         print("Minimaler Grauwert des korrigierten Bildes", out.min())
         print("Maximaler Grauwert des korrigierten Bildes", out.max())
     return out

def convert_world_file_to_pixel(utm_coord, world_file_name):
	#Nimmt referenzierte Koordinaten, und berechnet Pixel-Koordinaten mit Hilfe des World-Files
	#Structure of a world file:
	#Line 1: A: pixel size in the x-direction in map units/pixel
	#Line 2: D: rotation about y-axis
	#Line 3: B: rotation about x-axis
	#Line 4: E: pixel size in the y-direction in map units, almost always negative[3]
	#Line 5: C: x-coordinate of the center of the upper left pixel
	#Line 6: F: y-coordinate of the center of the upper left pixel

	out=[]
	temp=[]

	#Auslesen der Parameter aus dem World File
	try:
		f = open(world_file_name,'r')
		print("Lese aus Worldfile: " , world_file_name)
		for line in f:
			temp.append(line.strip())
		pixel_size_x=float(temp[0])
		pixel_size_y=float(temp[3])
		upper_left_x=float(temp[4])
		upper_left_y=float(temp[5])

	except:
		print("Fehler beim Einlesen des World-Files!")
		return

	#Umrechnen der Parameter auf Pixel: Hier ist eine Ungenauigkeit drin, Nachkommastellen werden am Ende ignoriert.

	for i in range(len(utm_coord)):
		pixel_y = (upper_left_y - utm_coord[i][0]) / pixel_size_y
		pixel_y = abs(int(pixel_y))
		pixel_x = (utm_coord[i][1] - upper_left_x) / pixel_size_x
		pixel_x = abs(int(pixel_x))
		out.append((pixel_y, pixel_x))

	return out

def convert_pixel_to_world_file(pixel_coord, world_file_name):

	out=[]
	temp=[]

	#Auslesen der Parameter aus dem World File
	try:
		f = open(world_file_name,'r')
		print("Lese aus Worldfile: " , world_file_name)
		for line in f:
			temp.append(line.strip())
		pixel_size_x=float(temp[0])
		pixel_size_y=float(temp[3])
		upper_left_x=float(temp[4])
		upper_left_y=float(temp[5])

	except:
		print("Fehler beim Einlesen des World-Files!")
		return

	#Berechnen der Koodinaten aus den Pixel
	for i in range(len(pixel_coord)):
		utm_y = upper_left_y + (pixel_coord[i][0] * pixel_size_y)
		utm_x = upper_left_x + (pixel_coord[i][1] * pixel_size_x)
		out.append((utm_y, utm_x))

	return out

def read_xyfile_as_int_list(FILE_IN, DELIMITER):
	#Liest eine Datei zeilenweise ein und speichert die ersten beiden Werte als integer in einer Liste, erst der 2 und dann der erste Wert (y-x-Koordinaten)
	import os, sys, glob
	out=[]
	try:
		f = open(FILE_IN,'r')
	except:
		print("Kann Datei nicht öffen")
		sys.exit(1)

	for line in f:
		#jede Zeile an dem delimiter auftrennen, leerzeichen löschen
		temp=[x.strip() for x in line.split(DELIMITER)]
		y=float(temp[1])
		x=float(temp[0])
		#Für numpy müssen die y-Werte zuerst stehen!
		out.append((y, x))

	return out
