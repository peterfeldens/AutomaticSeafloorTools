#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 11:29:51 2017

READ  iow laser sizer data
Write data to CORE database

@author: peter
"""

import pandas as pd 
import numpy as np
import sys
sys.path.append('/home/peter/gdrive/dev/Functions')
import FUNCTIONS_FILE_SYSTEM as ffs
import FUNCTIONS_ARRAYS as fa
import FUNCTIONS_DATABASE as fd



###########################VARIABLES###########################################

IN_FOLDER = '/home/peter/gdrive/Projekte/Ostsee_Entwicklung/Hütelmoor_Darsser_Schwelle/sediments/Korngrößen_Kerne/C1/'
file_list = ffs.getfiles('MES', IN_FOLDER)

core = 'EMB160/C1'
method = 'IOW_Laser'

database = '/home/peter/gdrive/Databases/CORES.db'
table = 'GRAINSIZE'
write_to_database = 'no'

try_to_infer_sample_depth = 'yes'  #get sample depth from sample id
position_of_sample_depth_in_sample_id_field = 2

###############################################################################

def make_pandas_data_frame():
    #Make the empty data dataframe
    import pandas
    df = pandas.DataFrame({
                                   'MESHES' :[],
                                   'GRAINSIZE_CUM' : [],
                                   'GRAINSIZE_HIST' : [],
                                   'SAMPLE_ID' : [],
                                   'SAMPLE_DEPTH' : [],
                                   'CORE_ID' : [],
                                   'METHOD' : [],
                                })
    return df




def add_phi(df,faktor = 1, column = 'MESHES', newcolumn='MESHES_PHI'):
    df[newcolumn] = -1 *  np.log2(df[column]/faktor)
    return df

def make_histogram_from_cumulative(df, cum_col = 'GRAINSIZE_CUM', hist_col = 'GRAINSIZE_HIST'):
    for i in range(df.shape[0]):
        if i == 0:
            df.loc[i, hist_col] = df.loc[i, cum_col]
        else:
            df.loc[i, hist_col] = df.loc[i, cum_col] - df.loc[i-1, cum_col]
    return df


def make_df_for_single_file_iow_laser_scanner(datei, core, method, position_of_sample_depth_in_sample_id_field ='NaN'):
    df_file = pd.read_csv(datei, names = ['data'])
    
    # Get used mesh sizes
    meshes = df_file.iloc[43:143]
    meshes.reset_index(inplace=True, drop = True)
    meshes = pd.to_numeric(meshes['data'])
    
    # Get cumulative volume percentage
    sizes = df_file.iloc[144:]
    sizes.reset_index(inplace=True, drop = True)
    sizes = pd.to_numeric(sizes['data'])
    
    # Konvert mesh sizes to PHI
    meshes_phi = 1 *  np.log2(meshes/1000)  # is missing

    #Resample to 1/4 PHI
    meshes_new, sizes_new = fa.resample_1D_array(meshes_phi,sizes)
    meshes_new = -meshes_new  #Um auf die richtrige PhioSkala zu kommen
    

    df = make_pandas_data_frame()
    df['MESHES'] = meshes_new
    df['GRAINSIZE_CUM'] = sizes_new
    
    name = df_file.iloc[4][0]
    df['SAMPLE_ID']= name
    df['CORE_ID']= core
    df['METHOD']= method
    df = make_histogram_from_cumulative(df)
    
    if try_to_infer_sample_depth == 'yes':
        try:
            temp = df.SAMPLE_ID.str.extractall('(\d+)')
            print temp[0][:,position_of_sample_depth_in_sample_id_field]
            sampledepth = temp[0][:,position_of_sample_depth_in_sample_id_field]
            df['SAMPLE_DEPTH']= sampledepth
        except:
            df['SAMPLE_DEPTH']= 'NaN'
            print 'ERROR MOST LIKELY INCONCISTENT SAMPLE LABELING IN RESULT FILES'
    return df



#%%
df_result = make_pandas_data_frame()
for datei in file_list:
    if method == 'IOW_Laser':
        df = make_df_for_single_file_iow_laser_scanner(IN_FOLDER + datei, core, method, position_of_sample_depth_in_sample_id_field )
    
    df_result = df_result.append(df, ignore_index = True)
    
#%%
#Write to Database
if write_to_database == 'yes':
    print 'Write to Database', database, table
    fd.data_to_sql(df_result,database,table)


#%%
