#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 11:29:51 2017

Read Surface data dervied from sieving or
laser scanner data to database

@author: peter
"""

import pandas as pd
import numpy as np
import os
import sys
sys.path.append('/home/peter/gdrive/dev/Functions')
import FUNCTIONS_FILE_SYSTEM as ffs
import FUNCTIONS_ARRAYS as fa
import FUNCTIONS_DATABASE as fd
import sqlite3 as sq

#%%

###########################VARIABLES###########################################

IN_FOLDER = '/home/peter/gdrive/Databases/'
os.chdir(IN_FOLDER)
file_list = ffs.getfiles('MES', IN_FOLDER)


database = '/home/peter/gdrive/Databases/SURFACE.db'
table = 'Metadata'
write_to_database = 'yes'


###############################################################################

#%%
df = pd.read_csv('import.csv', index_col = False, sep = '\t')
df.head()

#%% only top of cores
df = df.loc[df['section'] == '0']
#%%
df = df[["Lat", "Long", "Cruise", "Date", "Stones", "Shells", "Totalweight", "TotalWeight_washed", "ID"]]
#df = df.drop(["Date", "Lat", "Long","section", "finefraction", "North", "East", "Cruise","Shells (g)", "Stones", "Dryweight_after_washed","Dryweight_bef_washed", "Shells"] , axis=1)
#%%
#Write to Database
if write_to_database == 'yes':
    print 'Write to Database', database, table
    fd.data_to_sql(df,database,table)


#%%
