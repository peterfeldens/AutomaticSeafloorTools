# -*- coding: utf-8 -*-


def splitlines(line,typ=int):
    import numpy as np
        # Splits a string line and maps to array with typ=typ
        # not working for strings of mixed type (string+float)
    try:
        line = line.strip()  # remove \n
        line = line.split(' ')  # split by spaces
        line = map(typ, line)
        line = np.asarray(line)
    except:
        print "Hello from function splitline. Cannot split line"
        return
    return line


def flatten( alist ):
    #flatten a nested list into one list 
    newlist = []
     for item in alist:
         if isinstance(item, list):
             newlist = newlist + flatten(item)
         else:
             newlist.append(item)
     return newlist