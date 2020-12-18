def calculate_shear_strength(dfresult, DATABASE='CORES.db'):
    # Calculation of undrained shear strength according to DIN 17892-6
    import pandas
    import sqlite3
    
    g=9.81 #m/s^2
    
    #Die Abfrage kann noch optimiert werden...
    Q = """
        SELECT *
        FROM fall_cones
            JOIN shear_strength
                ON shear_strength.cone_id = fall_cones.id
        """
    
    calc = read_database(Q, DATABASE)
    
    calc['penetration_mean'] = calc[['CONE_PENETRATION1', 
    'CONE_PENETRATION2', 'CONE_PENETRATION3', 
    'CONE_PENETRATION4',]].mean(axis=1)
    
    calc['penetration_std'] = calc[['CONE_PENETRATION1', 
    'CONE_PENETRATION2', 'CONE_PENETRATION3', 
    'CONE_PENETRATION4',]].std(axis=1)
    
    dfresult['undrained_shear_average'] = calc['CU'] * g * calc['CONE_WEIGHT'] \
                                        / (calc['penetration_mean']**2) 
    
    return dfresult

