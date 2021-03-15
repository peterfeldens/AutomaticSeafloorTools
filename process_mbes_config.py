##############################################################
# LEVEL 1: IMPORT AND BASIC CORRECTIONS
##############################################################
# Control which levels are worked on
LEVEL1 = 'yes'
LEVEL2 = 'no'
LEVEL3 = 'no'

####IMPORTANT NOTE
# To allow for the handling of the mb-system scheme for marking processed files
# survey lines MUST NOT END with the letter "p"
####IMPORTANT NOTE

remove_lock_files = 'yes' #Yes tries to remove lockfiles for all files linked in the datalists via mblist
PFAD = "/Users/peter/TeamDropbox/Paper/DeepLearning/2021_multidimensional/data/bsh_dataset_mbes"
rekursive_directory_search = 'no'
PREPROCESS = 'yes'
FORMAT = 89  # .ALL UND .S7K FILES  work
file_end = '.s7k'
SS_FORMAT = 'S'  # scbw  s snippet c calib. snippet b widebeambackscatter w calibwidebeambackscatter "auto" - no option

AREA = '10.729/10.757/54.50/54.55'
#AREA = '10/12/54/55' #WESN. printed in datalist.info at the end of level1
GENERATE_DATALIST = 'no'
AUTO_CLEAN_BATHY = 'no'
auto_clean_with_area_boundaries = 'no'
ATTITUDE_LAG = ''
SELECT_SVP = ''          # mbsvpselect crashing at the moment why?? -> mbsystem bug? has to be done manually atm
SVP = ''             #this is the manual file included in all par files
CORRECT_HPR='no'
ROLL_CORR = 0.00
PITCH_CORR = 0.00
CORRECT_TIDE = ''        #no: removes entries from par fileand reprocesses
TIDEFILE = ''  #Tidemode set to 2
CORRECT_DRAFT = ''
DRAFT_CORR = 0.0
INVERT_HEAVE = 'no' #this was reported to be sometimes wrong for NORBIT data


EXPORT_NAV = 'yes'           # Export Navigation information and stores under profile file name
EXPORT_INFO_LEVEL1 = 'no'   # write output of mbinfo to datalist.info (.e.g, for region boundaries)
##############################################################
# LEVEL 2: Correct Backscatter Data
##############################################################
EXPORT_ARC_CURVES = 'no'
PROCESS_SCATTER = 'yes'  # yes is running mbbackangle
CONSIDER_SEAFLOOR_SLOPE = 'no'
AVERAGE_ANGLE_CORR = 'yes' # backangle correction file specific (no) or average (yes) for complete datesaet

SSS_ACROSS_CUT = 'no'
#This is done via sed. If should only be run once,
# there are issues with replacing the DATACUT commands in the .par files otherwise
SSS_ACROSS_CUT_MIN = -25 #in m, negative is portside
SSS_ACROSS_CUT_MAX = 25 #in m

SSS_CORRECTIONS = 'yes' #applies all of the follwoing settings
SSSWATHWIDTH = 160  #that is supposed to e an agnle. I have no clue what happens
# but settings this to any value removes the beams where the roll claib failed...
SSINTERPOLATE = 0
EXPORT_INFO_LEVEL2 = 'no' ## write output of mbinfo to datalist.info (.e.g, for region boundaries)
##############################################################
# LEVEL 3: Make grid data
##############################################################

SCATTER_FILTER = ''       #low or high - high not implemented atm works on p-files



## Grids
WORK_ON_PER_FILE_BASIS = 'no'  # Make grids i.e. for each file individually

# The following settings are only for individual file processing. THe other one take educated guesses..
INTERPOLATION = '-C3/1'      #up to three cells are interpolated
GENERATE_BATHY_GRIDS = 'yes'
GENERATE_SCATTER_GRIDS = 'yes'
EXPORT_SCATTER_TIF = 'no'  #currently only for filtered file specific grids
SCATTER_WITH_FILTER ='yes'   #Export filtered grids
EXPORT_XYI_FROM_GRID = 'no'
BATHY_RES = '-E0.25/0.25'
SCATTER_RES = '-E0.25/0.25'
# convert Grids
UTM_CONVERT = 'yes'
UTM_ZONE = '-JUTM32N'   # in syntax for mbsystem
#Only for work on a per-file bases
EXPORT_BEAM_ANGLE = 'no'    #
EXPORT_XYI = 'no'           #
EXPORT_XYZ = 'no'
KFAKTOR = 50               # jeder wievielte Schuss soll exportiert werden mit EXPORT_XYI

FORCE_MBPROCESS = 'no'   #Force a mbprceoss run; only needed for manual changes
number_of_exceptions = 0
