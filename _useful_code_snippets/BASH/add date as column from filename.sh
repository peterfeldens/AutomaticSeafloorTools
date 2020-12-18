#!/bin/sh




#Einlesen aller sgy-Dateien im aktuellen Verzeichnis.


DATEILISTE=$(ls -1 *.txt)

for DATEI in $DATEILISTE

do

	out=$(basename $DATEI .txt) 
	#dos2unix
	sed $'s/\r$//' $DATEI > temp1
	awk -F "," ' NR >= 1 {print $0","substr(FILENAME,1,6)}' temp1 > temp2
	#unix2dos
	sed 's/$'"/`echo \\\r`/"  temp2 > $out.dateadded.csv
	rm temp1
	rm temp2


done

# print first character
# $ awk -F\| '$3 > 0 { print substr($3,1,6)}' file1