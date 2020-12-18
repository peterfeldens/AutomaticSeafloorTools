import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from skimage import data, img_as_float
from skimage import exposure

def generate_colors(i, k=1):
	#Generiert Farben
	from pylab import *
	cm = get_cmap('gist_rainbow')
	color = cm(1.*i/k)
	return color