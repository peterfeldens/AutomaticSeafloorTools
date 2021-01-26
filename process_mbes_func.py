##############################################################
# Functions
##############################################################
import os
def test_for_par_files(FORMAT, mbfile):
    # Work aorund to reate par files
    if os.path.isfile(mbfile + ".par"):
        print("Parameter file exist")
    else:
        print("Parameter file not existing for ", mbfile)
        command = "mbset -F" + "FORMAT" + " -I" + mbfile + " -PNAVMODE:1"
        os.system(command)
        command = "mbset -F" + "FORMAT" + " -I" + mbfile + " -PNAVMODE:0"
        os.system(command)


def test_for_processed_mbfiles(files):
    # Test if files already processed -> Test if inf files exists
    import pandas
    files_to_process = []
    for i in range(len(files)):
        test_file = files[i] + '.inf'
        test_case = os.path.isfile(test_file)
        if test_case == False:
            print('Bearbeite Datei: ', files[i])
            files_to_process.append(files[i])
            df = pandas.DataFrame(files_to_process)
            df.to_csv('last_import', header=False, index=False)
        else:
            print('Ignoriere Datei: ', files[i])
    return files_to_process


def export_scatter_file(SCATTERFILE):
    """Export Scatter files"""
    # Intensity Daten einlesen: Tabelle Intensity
    # X Y Intensity
    import pandas
    import sys
    DELIMITER = '\t'
    XPos = []
    YPos = []
    Intensity = []
    Depth = []
    Acrosstrack_Dist = []
    BeamAngle = []
    # FileName = []

    try:
        f = open(SCATTERFILE, 'r')
    except:
        print("Fehler in import_scatter_file")
        sys.exit(1)

    for line in f:
        # jede Zeile an dem delimiter auftrennen, leerzeichen löschen
        temp = [x.strip() for x in line.split(DELIMITER)]
        XPos.append(float(temp[0]))
        YPos.append(float(temp[1]))
        Intensity.append(float(temp[2]))
        Depth.append(float(temp[3]))
        Acrosstrack_Dist.append(float(temp[4]))
        BeamAngle.append(float(temp[5]))

        # FileName.append(str(SCATTERFILE))

    # Combine into Pandas Data Frame
    dfdata = pandas.DataFrame({
        'X': XPos,
        'Y': YPos,
        'Intensity': Intensity,
        'Depth_below_trans': Depth,
        'Acrosstrack_Dist': Acrosstrack_Dist,
        'BeamAngle': BeamAngle,
    })
    f.close()
    return dfdata


def export_grid_file(SCATTERFILE, TYPE):
    """Export grid files"""
    # Intensity Daten einlesen: Tabelle Intensity
    # X Y Intensity - das sollen doch grids werden.....
    import pandas
    import sys
    DELIMITER = '\t'
    XPos = []
    YPos = []
    Z = []

    try:
        f = open(SCATTERFILE, 'r')
    except:
        print("Fehler in import_scatter_file")
        sys.exit(1)

    for line in f:
        # jede Zeile an dem delimiter auftrennen, leerzeichen löschen
        temp = [x.strip() for x in line.split(DELIMITER)]
        XPos.append(float(temp[0]))
        YPos.append(float(temp[1]))
        Z.append(float(temp[2]))

        # FileName.append(str(SCATTERFILE))

    # Combine into Pandas Data Frame
    dfdata = pandas.DataFrame({
        'X': XPos,
        'Y': YPos,
        'Intensity': Z,
    })
    f.close()
    return dfdata


def process_scatter(FORMAT, mbfile, CONSIDER_SEAFLOOR_SLOPE):
    if CONSIDER_SEAFLOOR_SLOPE == 'yes':
        command = 'mbgrid -I datalistp.mb-1 -R1.2 -A2 -C40/3 -F1 -N -O ZTopoFullInt'
        os.system(command)
        command = 'mbbackangle -I' + mbfile + ' -F' + \
                  str(
                      FORMAT) + ' -A1 -A2 -Q -V -N87/86.0 -R50 -G1/85/80.0/85/100 -G2/85/25000.0/85/100 -R40 -T ZTopoFullInt.grd '
        os.system(command)
    else:
        command = 'mbbackangle -I' + mbfile + \
                  ' -F' + str(FORMAT) + ' -A1 -A2 -Q -V -N87/86.0 -R50 -G1/85/80.0/85/100 -G2/85/25000.0/85/100 -R40 '
        os.system(command)

    # Make mbset entries
    command = 'mbset -I' + mbfile + ' -F' + str(FORMAT) + ' PSSCORRTYPE: 1'
    os.system(command)
    return


def choose_processed_unprocessed_file(file_list):
    unprocessed_files = []
    processed_files = []
    processed_processed_files = []
    temp = []
    for i in file_list:
        if "p.mb" not in i:
            unprocessed_files.append(i)
        if "p.mb" in i:
            if "pp.mb" not in i:
                processed_files.append(i)
        if "pp.mb" in i:
            processed_processed_files.append(i)
    return unprocessed_files, processed_files, processed_processed_files


def mbprocess(FORMAT, mbfile):
    command = 'mbprocess  -F' + str(FORMAT) + ' -I' + mbfile
    os.system(command)
    return


def mbfilter(FORMAT, mbfilep):
    command = 'mbfilter -A2 -S2/5/3/1 -F' + str(FORMAT) + ' -I' + mbfilep
    os.system(command)
    return


def mbpreprocess(FORMAT, mbfile, SS_FORMAT):
    if SS_FORMAT == 'auto':
        command = command = 'mbpreprocess --format=' + \
                            str(FORMAT) + ' --input=' + mbfile
        os.system(command)
    else:
        command = command = 'mbpreprocess --format=' + \
                            str(FORMAT) + '  --multibeam-sidescan-source=' + \
                            str(SS_FORMAT) + ' --input=' + mbfile
        os.system(command)
    return


def execute_mbcommand(mbcommand):
    print("Execute: ", mbcommand)
    os.system(mbcommand)
    return


def autoclean(mbfile, FORMAT, autoclean_with_area_boundaries, AREA=''):
    if autoclean_with_area_boundaries == 'yes':
        command = 'mbclean -F' + str(FORMAT) + ' -I' + mbfile + ' -R3 -X5 -G0.9/1.1 -Q1 -Z -W' + AREA
        print("Runnig mbclean: Check if appropriate", command)
        os.system(command)
        command = 'mbvoxelclean --input=datalist.mb-1 --voxel-size=0.5/0.5 --occupy-threshold=5 --flag-empty --verbose'
        print("Runnig mbclean: Check if appropriate", command)
        os.system(command)
    else:
        command = 'mbclean -F' + str(FORMAT) + ' -I' + mbfile + ' -G0.9/1.1 -R3 -X20 -Q0.5 -Z'
        print("Runnig mbclean: Check if appropriate", command)
        os.system(command)
        command = 'mbareaclean -F' + str(FORMAT) + ' -I' + mbfile + ' -D1.5/10 -M0.1/10 -S5'
        print("Runnig mbareaclean: Check if appropriate", command)
        os.system(command)
    return


def bathy_grid_file(file, BATHY_RES, FORMAT, UTM_CONVERT, UTM_ZONE):
    if UTM_CONVERT == 'no':
        command = 'mbm_grid ' + BATHY_RES + ' -A2 -C2  -G3 ' + ' -F' + \
                  str(FORMAT) + ' -I' + file + \
                  ' ' + '-O' + file + '_bath'
        os.system(command)
    if UTM_CONVERT == 'yes':
        command = 'mbm_grid ' + BATHY_RES + ' -A2 -C2  -G3 ' + UTM_ZONE + ' -F' + \
                  str(FORMAT) + ' -I' + file + \
                  ' ' + '-O' + file + '_bath'
        os.system(command)
    command = './' + file + '_bath_mbgrid.cmd '
    os.system(command)
    return


def scatter_grid_file(file, SCATTER_WITH_FILTER, SCATTER_RES, INTERPOLATION, FORMAT, UTM_CONVERT, UTM_ZONE):
    name_add = ''
    print('Generate Scatter Grid for file:', file)
    datatype = '-A4'
    if SCATTER_WITH_FILTER == 'yes':
        print('Plotting grids of low-pass-filtererd SSS data')
        datatype = '-A4F'
        name_add = '_filtered'
    # Generate first cut sidescan mosaic and plot
    if UTM_CONVERT == 'no':
        command = 'mbm_grid ' + datatype + ' -M  -P0 -G3' + ' ' + SCATTER_RES + ' ' + INTERPOLATION + ' -F' + str(
            FORMAT) + ' -I' + file + ' ' + '-O' + file + '_sss' + name_add
        os.system(command)
    if UTM_CONVERT == 'yes':
        command = 'mbm_grid ' + datatype + ' -M  -P0 -G3' + ' ' + SCATTER_RES + ' ' + INTERPOLATION + ' ' + UTM_ZONE + ' -F' + str(
            FORMAT) + ' -I' + file + ' ' + '-O' + file + '_sss' + name_add
        os.system(command)
    if SCATTER_WITH_FILTER == 'yes':
        command = './' + file + '_sss_filtered_mbmosaic.cmd '
        os.system(command)
    if SCATTER_WITH_FILTER == 'no':
        command = './' + file + '_sss_mbmosaic.cmd '
        os.system(command)
    return


def export_arc(mbfile, FORMAT):
    command = "mblist -F" + str(FORMAT) + " -I" + str(mbfile) + " -NA -OXYNCd#.lb > " + mbfile + ".arc"
    os.system(command)