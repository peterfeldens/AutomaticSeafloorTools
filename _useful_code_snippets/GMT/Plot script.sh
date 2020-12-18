chris_plot.sh
Typ
Text
Größe
2 KB (2.105 Byte)
Belegter Speicherplatz
2 KB (2.105 Byte)
Speicherort
GMT
Eigentümer
Ich
Geändert am
02.02.2017 von mir
Geöffnet am
12:52 von mir
Erstellt
23.08.2019 mit Insync
Beschreibung hinzufügen
Betrachter können die Datei herunterladen.

#!/bin/bash
#also see readme for parameters leading to grid creation
#cut bathy
#mbm_grid -F-1 -I chrislistp.mb-1 -A2 -E80/80 -Ochrisbathy -R$region
#region=-55.343569/-54.89759/42.18132/42.5
##plot sidescan grid
# make nice coor color scale -> needs to run only once
#gmt grdhisteq chrissss_cut.grd -Gchrissss_cut_smooth -N -V
#gmt grdcut smooth_chris.grd -Gsmooth_chris_cut.grd -R$region
#gmt grdcut chrisbathy.grd -Gchrisbathy_cut.grd -R$region  
#dirty plot



#plot backscatter:
#- ADD 
#-MNIdatalist to plot navigation data
#- S for histogram equalization


GMTDEF='-MGDFONT_ANNOT_PRIMARY/12,Helvetica,black -MGDFONT_ANNOT_SECONDARY/10,Helvetica,black -MGDFONT_LABEL/12,Helvetica,black -MGDFONT_TITLE/14,Helvetica,black'
ZONE='-PC6$'

mbm_grdplot -L'Backscatter Data' -Ichrissss_cut_smooth.grd -G1 $ZONE  -D -W2/4 -MGLfx0.5/0.3/center/3km+l'km' -MGQ300 -MXG255/0/0 -MXSc0.075 -MXIcore_chris_fig.csv -Obackscatter_smooth $GMTDEF
./backscatter_smooth.cmd

mbm_grdplot  -L'Backscatter Data' -Ichrissss_cut_smooth.grd -G1 $ZONE  -D -W2/4 -MGLfx0.5/0.3/center/3km+l'km' -MGQ300 -MXG255/0/0 -MXSc0.075 -MXIcore_chris_fig.csv -Z-2/2/1 -Obackscatter_contrast -S $GMTDEF
./backscatter_contrast.cmd

convert -background white -alpha remove -alpha off -density 400 backscatter_smooth.ps -resize 100% -quality 92  backscatter_smooth.jpg 
convert -background white -alpha remove -alpha off -density 400 backscatter_contrast.ps -resize 100% -quality 92  backscatter_contrast.jpg

#bathy_plot
mbm_grdplot -L'Bathymetry' -Ichrisbathy_cut.grd $ZONE  -A0.1/315 -G2  -W1/1 -MGLfx0.5/0.3/center/3km+l'km' -MGQ300 -MXG0/0/0 -MXSc0.075 -MXIcore_chris_fig.csv -MXSN -MXW5 -MXIprofile_figure_chris.txt  -Obathy $GMTDEF
./bathy.cmd

mbm_grdplot -L'Navigation' -Ichrisbathy_cut.grd $ZONE -A0.1/315 -G2  -W1/1 -MGLfx0.5/0.3/center/3km+l'km' -MNIchrislistp.mb-1 -Obathy_nav $GMTDEF
./bathy_nav.cmd

convert -background white -alpha remove -alpha off -density 400 bathy.ps  -resize 100% -quality 92  bathy.jpg
convert -background white -alpha remove -alpha off -density 400 bathy_nav.ps  -resize 100% -quality 92  bathy_nav.jpg
