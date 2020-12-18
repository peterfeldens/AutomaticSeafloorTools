def getfiles(ID='', PFAD='.'):
    # Gibt eine Liste mit Dateien in PFAD und der Endung IDENTIFIER aus.
    import os
    import sys
    files = []
    for file in os.listdir(PFAD):
        if file.endswith(ID):
            print(file)
            files.append(str(file))
    return files