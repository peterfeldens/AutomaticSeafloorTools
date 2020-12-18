# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:33:38 2016

@author: feldens
"""

    
def data_to_sql(DATAFRAME, DATABASE, TABLE,INDEX=False):
    import sqlite3 as sq
    conn = sq.connect(DATABASE)
    DATAFRAME.to_sql(TABLE,conn, if_exists='append', index = INDEX)
    conn.close()
    return
    
def filter_for_duplicates(DATABASE, TABLE):
    import sqlite3 as sq
    #Working Sample Only with manual entry until now
    conn = sq.connect(DATABASE)
    c = conn.cursor()
    # sql get list of all column names in table -> then feed that for filtering
    # Execute
    c.execute('DELETE FROM SHEAR_STRENGTH WHERE rowid NOT IN (SELECT min(rowid) FROM SHEAR_STRENGTH GROUP BY CORE_ID, CORE_DEPTH, METHOD, TYPE )')

    # Save (commit) the changes
    conn.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    return
    
def filter_for_empty(DATABASE, TABLE):
    import sqlite3 as sq
    #Working Sample Only with manual entry until now
    conn = sq.connect(DATABASE)
    c = conn.cursor()
    # sql get list of all column names in table -> then feed that for filtering
    # Execute
    c.execute('DELETE FROM Results WHERE Greylevels IS NULL OR TRIM(X) = ''')

    # Save (commit) the changes
    conn.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    return
    
    
def get_image_list(Q = """SELECT * FROM metadata JOIN images ON metadata.id = images.core_id;""",DATABASE='CORES.db',TABLE='IMAGES', RELPATH = './CORES_IMAGES/'):
    #Wenn kein Q übergeben wird eine Liste der Filelinks mit allen verfügbaren Photos ausgegeben
    dfresult = read_database(Q)
    corephotos = dfresult['FILELINK'].tolist()
    for i in range(len(corephotos)):
        corephotos[i] = RELPATH + corephotos[i]   
    return corephotos

def read_database(Q, DATABASE='CORES.db', param=None):
   import sqlite3 as sq
   import pandas
   conn = sq.connect(DATABASE)
   dfresult = pandas.read_sql_query(Q,conn, params=param)
   conn.close()
   return dfresult 


    #%% Create database
"""
conn = sq.connect(DATABASE)
cursor = conn.cursor()
try:
    cursor.execute('''CREATE TABLE Metadata(FileName Text PRIMARY KEY, 
                                            Freq INTEGER) 
                    ''')
    conn.commit()
    cursor.execute(''' CREATE TABLE BeamAngle(PingNumber Int,
                                              FileName Text,
                                              BeamAngle Real,
                                              BeamNumber Int,
                                              BeamX Real,
                                              BeamY Real,
                                              BeamZ Real,
                                              ID PRIMARY KEY AUTOINCREMENT
                                              FOREIGN KEY BeamAngle(FileName) REFERENCES Metadata(FileName)
                                              )
                    ''')
    conn.commit()
except:
    print('Could not create database file, exists already')
finally:
    conn.close()
    
#
"""