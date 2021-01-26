##############################################################
##############################################################
#
# Example processing of Norbit s7k data
#
##############################################################
##############################################################
#
# Preprocess the logged data
#
# Generate datalist of logged data files
mbm_makedatalist -S.s7k -Odatalistl.mb-1

# Preprocess the s7k data logged by Reson 7kcenter
mbpreprocess  --input=datalistl.mb-1 \
                --verbose

# Get datalist of raw *.mb89 files plus ancilliary files
mbm_makedatalist -S.mb89 -P -Odatalist.mb-1 -V
mbdatalist --update-ancilliary --datalistp --verbose

# Generate raw topography grid
mbgrid -I datalist.mb-1 -A2 -F1 -C10 -N -O ZTopoRaw -V
mbgrdviz -I ZTopoRaw.grd &

# Get tide models and set for use by mbprocess
#mbotps -A1 -M -V -Idatalist.mb-1

# To test bathymetry recalculation use sound speed model from mbvelocitytool
#mbset -PSVPFILE:20200527_1431.svp

# Set sonar draft
mbset -PDRAFTOFFSET:3.8

# Reverse sign of heave data - not sure if the sign error is an error in the data
# or an error in the code recognizing the convention for this particular data source
#mbset -PHEAVEMULTIPLY:-1

# Offset navigation source relative to sonar on platform
# mbset -PNAVOFFSETX:1.305 -PNAVOFFSETY:0.0

# Process the 7k data
mbprocess -C4

# Edit bathymetry
# mbclean -Y-100/100
# mbedit -I datalist.mb-1
# mbeditviz -I datalist.mb-1

# Generate first cut grid with interpolation for backscatter and sidescan correction
mbgrid -I datalistp.mb-1 -R1.2 -A2 -C40/3 -F1 -N -O ZTopoFullInt -V
mbgrdviz -I ZTopoFullInt.grd &

# calculate correction functions for mutibeam amplitude and multibeam sidescan data
mbbackangle -I datalist.mb-1 \
	-T ZTopoFullInt.grd \
	-A1 -A2 -Q -V -N87/86.0 -R50 -G1/85/80.0/85/100 -G2/85/25000.0/85/100
mbset -PAMPCORRFILE:datalist.mb-1_tot.aga -PSSCORRFILE:datalist.mb-1_tot.sga

# Process the 7k data again
mbm_multiprocess

# Filter the sidescan
mbfilter -I datalistp.mb-1 -A2 -S2/5/3/1 -V

##############################################################
# Generate grids, mosaics, and maps from multibeam
##############################################################

# Generate raw topography grid
mbgrid -I datalist.mb-1 -A2 -C10 -F5 -N -O ZTopoRaw -V
mbgrdviz -I ZTopoRaw.grd &

# Generate processed topography grid
mbgrid -I datalistp.mb-1 -A2 -C10 -F5 -N -O ZTopo -V
mbgrdviz -I ZTopo.grd &

# Generate processed topography grid in square UTM coordinates
mbgrid -I datalistp.mb-1 -A2 -JU -C10 -F5 -N -O ZTopoUTMSq -V
mbgrdviz -I ZTopoUTMSq.grd &

# Topo slope navigation map
mbm_grdplot -I ZTopo.grd \
	-O ZTopoSlopeNav \
	-G5 -D0/1 -A1.0 \
	-L"Test s7k Data Processing":"Topography (meters)" \
	-MGLfx4/1/54/0.1+l"km" \
	-MNIdatalistp.mb-1 \
	-Pc -V
ZTopoSlopeNav.cmd
gmt psconvert ZTopoSlopeNav.ps -Tj -E300 -A -P

# Topo slope map
mbm_grdplot -I ZTopo.grd \
	-O ZTopoSlope \
	-G5 -D0/1 -A1.0 \
	-L"Test s7k Data Processing":"Topography (meters)" \
	-MGLfx4/1/54/0.1+l"km" \
	-Pc -V
ZTopoSlope.cmd
gmt psconvert ZTopoSlope.ps -Tj -E300 -A -P

# Topo 1 m contour topography map
mbm_grdplot -I ZTopo.grd \
	-O ZTopoCont \
	-G1 -C5 -MCW0p -A2 \
	-L"Test s7k Data Processing":"Topography (meters)" \
	-MGLfx4/1/54/0.1+l"km" \
	-Pc -V
ZTopoCont.cmd
gmt psconvert ZTopoCont.ps -Tj -E300 -A -P

# UTM GeoTiff slope image for GIS
mbm_grdtiff -I ZTopoUTMSq.grd \
	-O ZTopoUTMSq_Slope \
	-G5 -D0/1 -A1.0 -S -V
ZTopoUTMSq_Slope_tiff.cmd

# Multibeam amplitude
mbmosaic -I datalistp.mb-1 -A3 -N -Y5 -F0.05 -O ZAmpC -V
mbm_grdplot -I ZAmpC.grd \
	-O ZAmpCPlot \
	-G1 -W1/4 -D \
	-L"Test s7k Data Processing":"Multibeam Amplitude" \
	-MGLfx4/1/54/0.1+l"km" \
	-Pc -V
ZAmpCPlot.cmd
gmt psconvert ZAmpCPlot.ps -Tj -E300 -A -P

# Multibeam sidescan
mbmosaic -I datalistp.mb-1 -A4F -N -Y5 -C5 -F0.05 \
	-O ZMbssC -V
mbm_grdplot -I ZMbssC.grd \
	-O ZMbssCPlot \
	-G1 -W1/4 -D \
	-L"Test s7k Data Processing":"Corrected and Filtered Multibeam Backscatter" \
	-MGLfx4/1/54/0.1+l"km" \
	-Pc -V
ZMbssCPlot.cmd
gmt psconvert ZMbssCPlot.ps -Tj -E300 -A -P


##############################################################
