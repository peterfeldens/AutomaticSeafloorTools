#!/bin/sh
#Skript import archvie segy data (parasound) over SU to KS
# No data processing done at the moment



#Einlesen aller sgy-Dateien im aktuellen Verzeichnis.


DATEILISTE=$(ls -1 *.csv)

for DATEI in $DATEILISTE

do

	out=$(basename $DATEI .csv)
	awk 'NR==1 || NR % 35 ==0 ' $DATEI > $out.reduced.csv

	#sed 's/$'"/`echo \\\r`/"  temp > $out.reduced.csv
	rm temp

done