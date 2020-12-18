#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 16:15:37 2017

VISUALIZE core data

@author: peter
"""


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
sys.path.append('F:/GoogleDrive/dev/Functions')
import FUNCTIONS_DATABASE as fd
import FUNCTIONS_CORE as fc

#%%
database = 'F:/GoogleDrive/Databases/CORES.db'
#core = ['EMB160_C3', 'EMB160_C1']
core = ['EMB160_C1']

##############
plot_grain_size = 'yes'
include_mode = 'yes'
plot_age_control = 'yes'


plot_all_in_one = 'yes'
figsize = (2,6)
#############FIX VARIABLES

xcoords_sed = [8,4,2,1,-1]
# Generate color space with length of core
colors = cm.terrain(np.linspace(0, 1, len(core)))


#%
if plot_all_in_one == 'yes':
    plt.figure(figsize=figsize, dpi=100)


for core, c in zip(core, colors):   # c enumerates the colors to have them consistent for each core
    
    if plot_all_in_one == 'no':
        plt.figure(figsize=figsize, dpi=100)
        
    if plot_grain_size == 'yes':
        Q = """SELECT * 
                FROM metadata
                JOIN grainsize ON metadata.id = grainsize.core_id
                WHERE metadata.id ='""" + core + """'"""
                
        df = fd.read_database(Q, database)
    
        mean, sd, sample_depth, sample, mode1 = fc.get_mean_and_sd(df)
        
        
        grainsize_data = np.vstack((mean,sd,sample_depth, mode1))
        grainsize_data = grainsize_data.transpose()
        grainsize_data = grainsize_data[grainsize_data[:,2].argsort()]  # sort for sample depth
    
        # Plot grain size mean
        plt.plot(grainsize_data[:,0], grainsize_data[:,2], label = core + ' Mean', c=c)
        
        if include_mode == 'yes':
            plt.scatter(grainsize_data[:,3], grainsize_data[:,2], label='Mode', c=c)
        # PLot standard deviation
        plt.errorbar(grainsize_data[:,0], grainsize_data[:,2], xerr=grainsize_data[:,1], fmt='+', c=c)

    
    #%%Read Age control
    if plot_age_control == 'yes':
        Q = """SELECT * 
                FROM metadata
                JOIN age_control ON metadata.id = age_control.core_id
                WHERE metadata.id ='""" + core + """'"""
                
        df = fd.read_database(Q, database)
        # Get relevant values as arrays
        age_control_depth = df.CORE_DEPTH.as_matrix()
        age_control_phi = np.zeros(len(age_control_depth))
        age_control_text = df.AGE_CONVENTIONAL
        
        age_control_data = np.vstack((age_control_phi, age_control_depth, age_control_text))
        age_control_data = age_control_data .transpose()
        age_control_data  = age_control_data[age_control_data[:,1].argsort()] 
        
        plt.plot(age_control_phi, 
                 age_control_depth, 
                 linestyle = '', 
                 marker='o', 
                 c=c)
        # ANnotate
        for i in range(len(age_control_depth)):
            plt.annotate(age_control_text[i], 
                         (age_control_phi[i] , age_control_depth[i]), 
                         (age_control_phi[i]-1, age_control_depth[i]-1),
                          arrowprops=dict(facecolor='black', shrink=0.05),
                          )
    

    ##########################################################################
    #Finalise individual plots
    if plot_all_in_one == 'no':
        #Finish Plot
        for xc in xcoords_sed: plt.axvline(x=xc, alpha=0.5)
        
        plt.xlim(4.0, -1)
        plt.title(core)
        #Axis work
        plt.gca().set_xlabel('Grain Size PHI')
        plt.gca().set_ylabel('Core depth [cm]')
        plt.gca().invert_yaxis()
        plt.show()
    
#%%
if plot_all_in_one == 'yes':
    #Finish Plot
    for xc in xcoords_sed: plt.axvline(x=xc, alpha=0.5)
    
    plt.xlim(4.0, -1)
    plt.title('Grain Size Data')
    plt.legend(loc='lower right')
    #Axis work
    plt.gca().set_xlabel('Grain Size PHI')
    plt.gca().set_ylabel('Core depth [cm]')
    plt.gca().invert_yaxis()
    plt.show

