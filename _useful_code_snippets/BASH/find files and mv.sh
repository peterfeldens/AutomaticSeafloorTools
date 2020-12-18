not recursively

find path_A -maxdepth 1 -name "*AAA*" -exec mv {} path_B \;

If you want to search all files recursively in path_A:

find path_A -name " " -exec cp {} /Volumes/Arbeit_X5/Arkona_Seis/ses/ \;

inlcude -type f to find only files