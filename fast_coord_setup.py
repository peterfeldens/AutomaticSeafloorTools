# Import libraries
import setuptools
import Cython.Build
import numpy as np
# Compile Cython files
setuptools.setup(name = 'fast_coord', ext_modules = Cython.Build.cythonize('fast_coord.pyx'), include_dirs=[np.get_include()])
