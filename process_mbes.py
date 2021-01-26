# -*- coding: utf-8 -*-
from __future__ import print_function  # python 3 print stements

"""
Created on Thu Sep 29 14:01:24 2016

@author: feldens
"""
##############################################################
# Multibeam processing script
# The calibrated s7k files need a three step approach.

# Parameters are set in the accomapnying file mbsystem_config.py
# Useage:
# python PROCESSING_MBSYSTEM.py mbsystem_config.py

##!!!! The filename of the profile lines MUST NOT END with a p !!!!
##!!! No spaces are allowed in the profile names or paths !!!

# todo scatter grid for dataset auf def umstellen
# todo implement high pass filter to improve stones
# todo allow the important of any config file to allow storing survey-configs

# This script is intended to only work on survey level datafiles.
# Do not use recursive datalists, things like mbbackangle and
# soi on will not handle that when used with this script.
##############################################################
# Preparation
##############################################################
# Load modules
import multiprocessing
from joblib import Parallel, delayed
import sys
import os
import automatic_seafloor_functions as asf
import process_mbes_func as pmf
from tqdm import tqdm

##############################################################
# Load Config File
##############################################################
# parser = argparse.ArgumentParser()
# Required Arguments
# parser.add_argument('config_file', type=str, help="Link to File with variables without .py extenstion")
# try:
#    options = parser.parse_args()
# except:
#    parser.print_help()
#    sys.exit(0)

# args = parser.parse_args()
# print("Importing settings from: ", args.config_file)
# config = args.config_file


# Really crude importing
from process_mbes_config import *

##############################################################
# Multiprocessing Setup
##############################################################
num_cores = multiprocessing.cpu_count() - 2
if num_cores < 2:
    print("Go buy a new PC")
    sys.exit(0)
print("Using ", num_cores, " cores. ")

# Pfade
os.chdir(PFAD)

# Delete old lock files
if remove_lock_files == 'yes':
    print("Trying to remove old lock files:")
    command = "mbdatalist -F-1 -Idatalist.mb-1 -Y"
    os.system(command)
    command = "mbdatalist -F-1 -Idatalistp.mb-1 -Y"
    os.system(command)
    command = "mbdatalist -F-1 -Idatalistpp.mb-1 -Y"
    os.system(command)
##############################################################
# Sanity checks
##############################################################
if SS_FORMAT not in ["S", "C", "auto", "W", "B"]:
    print("Select correct SS_Format identifier - refer to man mbpreprocess")
    sys.exit(0)

if UTM_CONVERT not in ["yes", "no"]:
    print("UTM_CONVERT must be yes or no")
    sys.exit(0)

if SCATTER_WITH_FILTER not in ["yes", "no"]:
    print("SCATTER_WITH_FILTER must be yes or no. Do it or do it not. There is no try")
    sys.exit(0)


###############################################################################
##############################################################
# LEVEL 1: IMPORT AND BASIC CORRECTIONS
##############################################################
# Preprocessing of data
DATA_TO_PROC = 'no'
print("Level 1 processing is set to:", LEVEL1)
if LEVEL1 == 'yes':
    if PREPROCESS == 'yes':
        if rekursive_directory_search == 'no':
            print('Preprocessing')
            # Hysweeppreprocess muss jede Datei einzeln vorgesetzt bekommen sonst wirds nichts
            s7kfiles = asf.getfiles(file_end)
        elif rekursive_directory_search == 'yes':
            s7kfiles = asf.getfiles(file_end, '.', 'yes')
        else:
            print("ERROR in PREPROCESS REKURSEIVE SEARCH SETTING")
            sys.exit(0)

        Parallel(n_jobs=num_cores)(delayed(pmf.mbpreprocess)(FORMAT, mbfile, SS_FORMAT)
                                   for mbfile in tqdm(s7kfiles))
        GENERATE_DATALIST = 'yes'

    if GENERATE_DATALIST == 'yes':
        #
        if rekursive_directory_search == 'no':
            print('Generate datalists non-recursive')
            command = '/bin/ls -1 *[^p].mb' + str(FORMAT) + ' | awk \'{print $1" ' + str(
                FORMAT) + '"}\' > datalist.mb-1'
            print(command)
            os.system(command)

        if rekursive_directory_search == 'yes':
            print('Generate datalists recursive')
            command = 'find . -type f -name "*.mb' + str(FORMAT) + '" | awk \'{print $1" ' + str(
                FORMAT) + '"}\' > datalist.mb-1'
            os.system(command)

        # Generate a datalist referencing processed mb201 files named datalistp.mb-1
        command = 'mbdatalist -Z -I datalist.mb-1'
        os.system(command)

    # test for par files level 1
    ID = 'mb' + str(FORMAT)
    if rekursive_directory_search == 'no':
        files = asf.getfiles(ID)
    if rekursive_directory_search == 'yes':
        files = asf.getfiles(ID, '.', 'yes')
    files, _, _ = pmf.choose_processed_unprocessed_file(files)
    for mbfile in files:
        pmf.test_for_par_files(FORMAT, mbfile)

    if AUTO_CLEAN_BATHY == 'yes':
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        files, _, _ = pmf.choose_processed_unprocessed_file(files)
        print("Autoclean")
        Parallel(n_jobs=num_cores)(delayed(pmf.autoclean)(mbfile, FORMAT, auto_clean_with_area_boundaries, AREA)
                                   for mbfile in tqdm(files))
        DATA_TO_PROC = 'yes'

    if ATTITUDE_LAG == 'yes':
        # ---------------------------------------------------------------------------------
        # check the attitude time lag
        # ---------------------------------------------------------------------------------
        print('Checking for attitude lag')
        # Look for correlation between raw roll and apparent seafloor acrosstrack slope
        command = 'mbrolltimelag -I datalist.mb-1 -T501/-0.5/0.5 -K18 -N50 -O ZInitial -V'
        os.system(command)
        command = './ZInitial_timelaghist.txt.cmd'
        os.system(command)
        command = './ZInitial_timelagmodel.txt.cmd'
        os.system(command)
        command = './ZInitial_xcorr.txt.cmd'
        os.system(command)
        command = 'convert -density 300 ZInitial_timelaghist.txt.ps -trim -quality 92 ZInitial_timelaghist.txt.jpg'
        os.system(command)
        command = 'convert -density 300 ZInitial_timelagmodel.txt.ps -trim -quality 92 ZInitial_timelagmodel.txt.jpg'
        os.system(command)
        command = 'convert -density 300 ZInitial_xcorr.txt.ps -trim -quality 92 ZInitial_xcorr.txt.jpg'
        os.system(command)

    if EXPORT_NAV == 'yes':
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        files, _, _ = pmf.choose_processed_unprocessed_file(files)
        print("Exporting Navigation")
        for file in tqdm(files):
            command = 'mbnavlist -F' + str(FORMAT) + ' -I' + file + ' -D25 -G, > ' + file + '.navtemp'
            os.system(command)
            command = 'sed  "s/$/,' + str(file) + '/" ' + file + '.navtemp > ' + file + '.nav'
            os.system(str(command))
            command = 'rm ' + file + '.navtemp'
            os.system(command)

    if CORRECT_HPR == 'yes':
        print('Correct HPR')
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        files, _, _ = pmf.choose_processed_unprocessed_file(files)
        for mbfile in files:
            command = 'mbset -F' + str(FORMAT) + ' -I' + mbfile + ' -PROLLBIASMODE:1 -PROLLBIAS:' + str(
                ROLL_CORR) + ' -PPITCHBIASMODE:1 -PPITCHBIAS:' + str(PITCH_CORR)
            os.system(command)
        DATA_TO_PROC = 'yes'

    if CORRECT_DRAFT == 'yes':
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        files, _, _ = pmf.choose_processed_unprocessed_file(files)
        for mbfile in files:
            command = 'mbset -F' + str(FORMAT) + ' -I' + mbfile + ' -PDRAFTMODE:4 -PDRAFT:' + str(DRAFT_CORR)
            os.system(command)
        DATA_TO_PROC = 'yes'

    if SELECT_SVP == 'yes':
        print('Select SVP')
        # command = 'mbsvpselect -P1 -Ssvplist.mb-1'   #P1: selection to nearest in time
        # Workaround weil das mit den svpprofilen bei format 201 nicht zu gehen scheint
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        files, _, _ = pmf.choose_processed_unprocessed_file(files)
        for mbfile in files:
            command = 'mbset -F' + str(FORMAT) + ' -I' + mbfile + ' -PSVPMODE:1 -PSVPFILE:' + SVP
            os.system(command)
        DATA_TO_PROC = 'yes'

    if CORRECT_TIDE == 'yes':
        print('Correcting Tide')
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        files, _, _ = pmf.choose_processed_unprocessed_file(files)
        for mbfile in files:
            command = 'mbset -F' + str(FORMAT) + ' -I' + mbfile + ' -PTIDEMODE:1 -PTIDEFILE:' + str(
                TIDEFILE) + ' -PTIDEFORMAT:2'
            os.system(command)
        DATA_TO_PROC = 'yes'

    if CORRECT_TIDE == 'no':
        print('Not correcting Tide/removing tidal corrections')
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        files, _, _ = pmf.choose_processed_unprocessed_file(files)
        for mbfile in files:
            command = 'mbset -F' + str(FORMAT) + ' -I' + mbfile + ' -PTIDEMODE:0 -PTIDEFILE:'
            os.system(command)
        DATA_TO_PROC = 'yes'

    if INVERT_HEAVE == 'yes':
        command = 'mbset -PHEAVEMULTIPLY:-1'
        os.system(command)

    # Process if needed
    if FORCE_MBPROCESS == 'yes':
        DATA_TO_PROC = 'yes'

    if DATA_TO_PROC == 'yes':
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        files, _, _ = pmf.choose_processed_unprocessed_file(files)
        Parallel(n_jobs=num_cores)(delayed(pmf.mbprocess)(FORMAT, mbfile)
                                   for mbfile in tqdm(files))

        print('Generate datalists for processed files')
        if rekursive_directory_search == 'no':
            command = '/bin/ls -1 *[^p]p.mb' + str(FORMAT) + ' | grep -v "p.' + str(
                FORMAT) + '" | awk \'{print $1" ' + str(FORMAT) + '"}\' > datalistp.mb-1'
            os.system(command)
        if rekursive_directory_search == 'yes':
            command = 'find . -type f -name "*[^p]p.mb' + \
                      str(FORMAT) + '" | awk \'{print $1" ' + \
                      str(FORMAT) + '"}\' > datalistp.mb-1'
            os.system(command)
        if EXPORT_INFO_LEVEL1 == 'yes':
            print("Writing Basic information for datalist in datalist.info")
            command = "mbinfo -F-1 -Idatalist.mb-1 > datalist.info"
            os.system(command)
    DATA_TO_PROC = 'no'

##############################################################
# LEVEL 2: Backscatter information
##############################################################
print("Level 2 processing is set to:", LEVEL2)
if LEVEL2 == 'yes':

    # test for par files level 2
    ID = 'mb' + str(FORMAT)
    if rekursive_directory_search == 'no':
        files = asf.getfiles(ID)
    if rekursive_directory_search == 'yes':
        files = asf.getfiles(ID, '.', 'yes')
    _, files, _ = pmf.choose_processed_unprocessed_file(files)
    for mbfile in files:
        pmf.test_for_par_files(FORMAT, mbfile)

    if PROCESS_SCATTER == 'yes':
        print('Process Scatter')
        if AVERAGE_ANGLE_CORR == 'yes':
            print('Setting BS correction to a survey level')
            pmf.process_scatter("-1", "datalistp.mb-1", CONSIDER_SEAFLOOR_SLOPE)
            ID = 'mb' + str(FORMAT)
            if rekursive_directory_search == 'no':
                files = asf.getfiles(ID)
            if rekursive_directory_search == 'yes':
                files = asf.getfiles(ID, '.', 'yes')
            _, files, _ = pmf.choose_processed_unprocessed_file(files)
            for mbfile in files:
                print("updating mbset to survey level")
                command = 'mbset -F' + str(FORMAT) + ' -I' + mbfile + ' -PSSCORRFILE:datalistp.mb-1_tot.sga'
                os.system(command)
            DATA_TO_PROC = 'yes'
        else:
            print('Setting BS correction to a file level')
            ID = 'mb' + str(FORMAT)
            if rekursive_directory_search == 'no':
                files = asf.getfiles(ID)
            if rekursive_directory_search == 'yes':
                files = asf.getfiles(ID, '.', 'yes')
            _, files, _ = pmf.choose_processed_unprocessed_file(files)
            Parallel(n_jobs=num_cores)(delayed(pmf.process_scatter)(FORMAT, mbfile, CONSIDER_SEAFLOOR_SLOPE)
                                       for mbfile in tqdm(files))
            ID = '.mb' + str(FORMAT)
            if rekursive_directory_search == 'no':
                files = asf.getfiles(ID)
            if rekursive_directory_search == 'yes':
                files = asf.getfiles(ID, '.', 'yes')
            _, files, _ = pmf.choose_processed_unprocessed_file(files)
            for file in files:
                sga_name = file + '.sga'
                command = 'mbset -I' + file + ' -PSSCORRFILE:' + sga_name
                os.system(command)
        # Process the data
        DATA_TO_PROC = 'yes'

    if SSS_ACROSS_CUT == 'yes':
        print('Cutting SideScan Across Track')
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        _, files, _ = pmf.choose_processed_unprocessed_file(files)
        for mbfile in files:
            command = "gsed -i  \'s/DATACUT.*/DATACUT 2 2 -1000 " + str(SSS_ACROSS_CUT_MIN) + "\\nDATACUT 2 2 " + str(
                SSS_ACROSS_CUT_MAX) + " 1000 /\' " + mbfile + ".par"
            os.system(command)
        DATA_TO_PROC = 'yes'

    if SSS_CORRECTIONS == 'yes':
        print('Applying set SSS corrections')
        ID = 'mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        _, files, _ = pmf.choose_processed_unprocessed_file(files)
        for mbfile in files:
            # sed -i 's/search_string/replace_string/' filename
            # command = 'mbset -F' + str(FORMAT) + ' -I' + mbfile + ' PSSCORRMODE:1 -PSSSWATHWIDTH:' + \
            # str(SSSWATHWIDTH)  + ' -PSSINTERPOLATE:' + str(SSINTERPOLATE)
            command = "sed -i \"\" \'s/SSRECALCMODE.*/SSRECALCMODE 1/\' " + mbfile + ".par"
            os.system(command)
            command = "sed -i \"\" \'s/SSSWATHWIDTH.*/SSSWATHWIDTH " + str(SSSWATHWIDTH) + "/\' " + mbfile + ".par"
            os.system(command)
            command = "sed -i \"\" \'s/SSINTERPOLATE.*/SSINTERPOLATE " + str(SSINTERPOLATE) + "/\' " + mbfile + ".par"
            os.system(command)
        DATA_TO_PROC = 'yes'

    if EXPORT_ARC_CURVES == 'yes':
        print('Exporting ARC data')
        print("Angles cannot be correctly exported from mbsystem with the -NA side scan option as of 20.10.2020")
        print("Flat grazing angles need to be calculated in postprocessing until that time")
        ID = '.mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        _, files, _ = pmf.choose_processed_unprocessed_file(files)
        # mblist command to export arc
        Parallel(n_jobs=num_cores)(delayed(pmf.export_arc)(mbfile, FORMAT)
                                   for mbfile in tqdm(files))

    # Process if needed
    if FORCE_MBPROCESS == 'yes':
        DATA_TO_PROC = 'yes'

    if DATA_TO_PROC == 'yes':
        ID = 'p.mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')

        _, files, _ = pmf.choose_processed_unprocessed_file(files)
        Parallel(n_jobs=num_cores)(delayed(pmf.mbprocess)(FORMAT, mbfile)
                                   for mbfile in tqdm(files))
        # make pp-Datalist
        if rekursive_directory_search == 'no':
            print('Generate datalists for processed-processed files')
            command = '/bin/ls -1 *pp.mb' + str(FORMAT) + ' | grep -v "pp.' + str(
                FORMAT) + '" | awk \'{print $1" ' + str(FORMAT) + '"}\' > datalistpp.mb-1'
            os.system(command)

        if rekursive_directory_search == 'yes':
            command = 'find . -type f -name " *pp.mb' + \
                      str(FORMAT) + '" | awk \'{print $1" ' + \
                      str(FORMAT) + '"}\' > datalistpp.mb-1'
            os.system(command)
        if EXPORT_INFO_LEVEL2 == 'yes':
            print("Writing Basic information for datalist in datalistp.info")
            command = "mbinfo -F-1 -Idatalistp.mb-1 > datalistp.info"
            os.system(command)

    DATA_TO_PROC = 'no'
##############################################################
# LEVEL 3: Grids
##############################################################


print("Level 3 processing is set to:", LEVEL3)
if LEVEL3 == 'yes':
    if SCATTER_FILTER == 'low':
        ID = 'p.mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        _, _, files = pmf.choose_processed_unprocessed_file(files)
        print("LOW PASS FILTERING:")
        Parallel(n_jobs=num_cores)(delayed(pmf.mbfilter)(FORMAT, mbfile)
                                   for mbfile in tqdm(files))

    if SCATTER_FILTER == 'high':
        print('Highpass not yet implemented')
        SCATTER_WITH_FILTER = 'no'


    if WORK_ON_PER_FILE_BASIS == 'no': # this is from dave caress example processing script
        #Generate Navplot
        command = 'mbm_plot  -NF -O ZNavPlot'
        os.system(command)
        command = './ZNavPlot.cmd'
        os.system(command)

        # Generate raw topography grid
        command = 'mbgrid -I datalist.mb-1 -A2 -C10 -F5 -N -E0.25/0.25 -O ZTopoRaw -V'
        os.system(command)

        # Generate processed topography grid
        command = 'mbgrid -I datalistpp.mb-1 -A2 -C10 -F5 -N -E0.25/0.25 -O ZTopo -V'
        os.system(command)

        # Generate processed topography grid in square UTM coordinates
        command = 'mbgrid -I datalistpp.mb-1 -A2 -JU -C10 -F5 -N -E0.25/0.25 -O ZTopoUTMSq -V'
        os.system(command)

        # Topo slope navigation map
        command = 'mbm_grdplot -I ZTopo.grd -O ZTopoSlopeNav  -G5 -D0/1 -A1.0 -L"s7k Data Processing":"Topography (meters)"  -MGLfx4/1/54/0.1+l"km" -MNIdatalistpp.mb-1 -Pc -V'
        os.system(command)
        command = './ZTopoSlopeNav.cmd'
        os.system(command)
        command = 'gmt psconvert ZTopoSlopeNav.ps -Tj -E300 -A -P'
        os.system(command)

        # Topo slope map
        command = 'mbm_grdplot -I ZTopo.grd -O ZTopoSlope -G5 -D0/1 -A1.0 -L"s7k Data Processing":"Topography (meters)" -MGLfx4/1/54/0.1+l"km" -Pc -V'
        os.system(command)
        command = './ZTopoSlope.cmd'
        os.system(command)
        command = 'gmt psconvert ZTopoSlope.ps -Tj -E300 -A -P'
        os.system(command)

        # UTM GeoTiff slope image for GIS
        command = 'mbm_grdtiff -I ZTopoUTMSq.grd -O ZTopoUTMSq_Slope -G5 -D0/1 -A1.0 -S -V'
        os.system(command)
        command = './ZTopoUTMSq_Slope_tiff.cmd'
        os.system(command)

        # Multibeam amplitude
        command = 'mbmosaic -I datalistpp.mb-1 -A3 -N -Y5 -F0.05 -E0.25/0.25 -O ZAmpC -V'
        os.system(command)
        command = 'mbm_grdplot -I ZAmpC.grd -OZAmpCPlot  -G1 -W1/4 -D  -L"Test s7k Data Processing":"Multibeam Amplitude" -MGLfx4/1/54/0.1+l"km" -Pc -V'
        os.system(command)
        command = './ZAmpCPlot.cmd'
        os.system(command)
        command = 'gmt psconvert ZAmpCPlot.ps -Tj -E300 -A -P'
        os.system(command)

        # Multibeam sidescan
        command = 'mbmosaic -I datalistpp.mb-1 -A4F -N -Y5 -C5 -E0.25/0.25 -F0.05 -O ZMbssC -V'
        os.system(command)
        command = 'mbm_grdplot -I ZMbssC.grd -O ZMbssCPlot -G1 -W1/4 -D -L"Test s7k Data Processing":"Corrected and Filtered Multibeam Backscatter"  -MGLfx4/1/54/0.1+l"km" -Pc -V'
        os.system(command)
        command = './ZMbssCPlot.cmd'
        os.system(command)
        command = 'gmt psconvert ZMbssC.ps -Tj -E300 -A -P'
        os.system(command)

    if WORK_ON_PER_FILE_BASIS == 'yes':
        print('working on a per-file-basis')
        ID = 'p.mb' + str(FORMAT)
        if rekursive_directory_search == 'no':
            files = asf.getfiles(ID)
        if rekursive_directory_search == 'yes':
            files = asf.getfiles(ID, '.', 'yes')
        _, _, files = pmf.choose_processed_unprocessed_file(files)
        print('Folgende Dateien werden bearbeitet:', files)
        if GENERATE_BATHY_GRIDS == 'yes':
            Parallel(n_jobs=num_cores)(delayed(pmf.bathy_grid_file)(mbfile, BATHY_RES, FORMAT, UTM_CONVERT, UTM_ZONE)
                                       for mbfile in tqdm(files))

        if GENERATE_SCATTER_GRIDS == 'yes':
            print("Working on files: ", files)
            Parallel(n_jobs=num_cores)(
                delayed(pmf.scatter_grid_file)(mbfile, SCATTER_WITH_FILTER, SCATTER_RES, INTERPOLATION, FORMAT, UTM_CONVERT,
                                           UTM_ZONE)
                for mbfile in tqdm(files))

        if EXPORT_BEAM_ANGLE == 'yes':
            for file in files:
                print('Export Beam Angles for ', file)
                command = 'mblist -F' + str(FORMAT) + ' -I ' + file + ' -OXYg -MA -K' + str(
                    KFAKTOR) + '>  ' + file + '_ba.xya'
                os.system(command)

        if EXPORT_XYI_FROM_GRID == 'yes':
            if SCATTER_WITH_FILTER == 'yes':
                try:
                    print('Export filtered scatter from grid')
                    Parallel(n_jobs=num_cores)(delayed(pmf.execute_mbcommand)(
                        'gmt grd2xyz ' + str(mbfile) + '_sss_filtered.grd  > ' + str(mbfile) + '_sss_grid_filtered.xyi')
                                               for mbfile in files)
                except:
                    print('No filtered gridfile')
            else:
                try:
                    print('Export scatter from grid for ')
                    Parallel(n_jobs=num_cores)(delayed(pmf.execute_mbcommand)(
                        'gmt grd2xyz ' + str(mbfile) + '_sss.grd  > ' + str(mbfile) + '_sss_grid.xyi') for mbfile in
                                               files)
                except:
                    print('Problem with xyi export of file')

                    number_of_exceptions = number_of_exceptions + 1

        if EXPORT_XYI == 'yes':
            print("Export XYI")
            Parallel(n_jobs=num_cores)(delayed(pmf.execute_mbcommand)(
                'mblist -F' + str(FORMAT) + ' -I ' + mbfile + ' -O^X^Yb -JU -NA -K' + str(
                    KFAKTOR) + '  >  ' + mbfile + '_sss.xyi') for mbfile in files)

        if EXPORT_XYZ == 'yes':
            print("Export XYZ")
            Parallel(n_jobs=num_cores)(delayed(pmf.execute_mbcommand)('mblist -F' + str(FORMAT) + ' -I ' + mbfile +
                                                                  ' -O^X^YZ -JU -MA -K ' + str(
                KFAKTOR) + '  >  ' + mbfile + '_bath.xyz') for mbfile in files)
        print('All done')
