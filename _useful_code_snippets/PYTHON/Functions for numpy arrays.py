# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 04:36:47 2016

@author: Administrator
"""

def running_mean(x, N):
    # calculate running mean over N samples for array x
    import numpy as np
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def norm_negative_array(array):
    # norm a numpy array with negative numbers to a 0-1 Interval
    import numpy as np
    try:
        array_normed = (array - np.nanmin(array)) / np.nanmax(array - np.nanmin(array))
    except:
        print "Cannot norm array in fucntion norm_negative_array"
        return array
    return array_normed

def block_view(A, block= (3, 3)):
    """Provide a 2D block view to 2D array. No error checking made.
    Therefore meaningful (as implemented) only for blocks strictly
    compatible with the shape of A.
    from numpy import arange
    A= arange(144).reshape(12, 12)
    print block_view(A)[0, 0]
    #[[ 0  1  2]
    # [12 13 14]
    # [24 25 26]]
    print block_view(A, (2, 6))[0, 0]
    #[[ 0  1  2  3  4  5]
    # [12 13 14 15 16 17]]
    print block_view(A, (3, 12))[0, 0]
    #[[ 0  1  2  3  4  5  6  7  8  9 10 11]
    # [12 13 14 15 16 17 18 19 20 21 22 23]
    # [24 25 26 27 28 29 30 31 32 33 34 35]]"""
    # simple shape and strides computations may seem at first strange
    # unless one is able to recognize the 'tuple additions' involved ;-)
    from numpy.lib.stride_tricks import as_strided as ast
    shape= (A.shape[0]/ block[0], A.shape[1]/ block[1])+ block
    strides= (block[0]* A.strides[0], block[1]* A.strides[1])+ A.strides
    return ast(A, shape= shape, strides= strides)

def divisors(n):
    # get factors and their counts
    factors = {}
    nn = n
    i = 2
    while i*i <= nn:
        while nn % i == 0:
            if not i in factors:
                factors[i] = 0
            factors[i] += 1
            nn //= i
        i += 1
    if nn > 1:
        factors[nn] = 1

    primes = list(factors.keys())

    # generates factors from primes[k:] subset
    def generate(k):
        if k == len(primes):
            yield 1
        else:
            rest = generate(k+1)
            prime = primes[k]
            for factor in rest:
                prime_to_i = 1
                # prime_to_i iterates prime**i values, i being all possible exponents
                for _ in range(factors[prime] + 1):
                    yield factor * prime_to_i
                    prime_to_i *= prime

    # in python3, `yield from generate(0)` would also work
    for factor in generate(0):
        yield factor

def add_to_dict(dic, df, name):
    dic[name] = df
    return dic

def resample_1D_array(xold, yold, xmin=-5, xmax=5, step=0.25):
    import numpy as np
    assert np.all(np.diff(xold) > 0)
    xnew = np.arange(xmin,xmax,step)
    ynew = np.interp(xnew, xold, yold)
    return xnew, ynew


def idxquantile(s, q=0.5, *args, **kwargs):
    qv = s.quantile(q, *args, **kwargs)
    return (s.sort_values()[::-1] <= qv).idxmax()

def scale_numpy_array(array):
    from sklearn import preprocessing
    min_max_scaler = preprocessing.MinMaxScaler()
    array = min_max_scaler.fit_transform(array)
    return array

def image_stretch(img,greylevels, v=1):
    from sklearn.preprocessing import MinMaxScaler
    """
#Geht von einem 8bit Graustufenbild aus und reduziert es auf gewünschte Farbskala
#Das ist eigentlich noch ungenau, es müsste gerundet werden, und dann als Integer zurückgegeben

#factor=1./int(img.max())*(greylevels-1)
#a= img * factor
    greylevels = greylevels -1 #account for the 0
    img_min = img.min()
    img_max = img.max()
    img_std = (img -img_min) / (img_max - img_min)

    img_scaled = img_std * (greylevels - 0) + 0
    out=img_scaled.astype(int)

    if v==1:
        print("Minimaler Grauwert des korrigierten Bildes", out.min())
        print("Maximaler Grauwert des korrigierten Bildes", out.max())
    """
    scaler = MinMaxScaler(feature_range = (0,greylevels))
    scaler.fit(img)
    out = scaler.transform(img)

    return out

def contrast_stretch(img, percmin=2, percmax=98):
    # Contrast stretching
    import skimage
    import numpy as np
    pmin, pmax = np.percentile(img, (percmin, percmax))
    img_rescale = skimage.exposure.rescale_intensity(img, in_range=(pmin, pmax))
    return img_rescale

def contrast_equalization(img):
    # Equalization
    import skimage
    img_eq = skimage.exposure.equalize_hist(img)
    return img_eq

def adaptive_equalization(img):
    # Adaptive Equalization
    import skimage
    img_adapteq = skimage.exposure.equalize_adapthist(img)
    return img_adapteq

def make_search_array(infile, leafsize=25000, Y='Y', X='X'):
    import numpy as np
    from scipy.spatial import cKDTree
    search_array = np.array(infile[[Y,X]])
    # tree = cKDTree(search_array, leafsize=search_array.shape[0] +1)
    tree = cKDTree(search_array, leafsize = leafsize)
    return tree

def log0_10(x):
    import numpy as np
#Wir müssen Log von 0 als 0 definieren sonst bricht das alles zusammen.
    return np.where(x == 0., 0., np.log10(x))

def normalize_df_arbitrary_values(df, column, min_value, max_value, faktor = 1):
    #Needed to scale data to Baltic Sea Wide min/max values, and not the min/max values
    # in a given dataframe; to ensure comparability of different datasets
    print "Nue machen hier war ein Fehler drin richtiger code steht in funktion"
    df[column] = (df[column] - df[column].min()) / ( df[column].max() - df[column].min() ) * (max_value - min_value) + min_value 
    #new_value = ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
    return 

def normalize_df(df, column, faktor = 1):
    result = df.copy()
    max_value = df[column].max()
    min_value = df[column].min()
    result[column] = ((df[column] - min_value) / (max_value - min_value)) * faktor
    return result

def convert_from_categorical(df, column):
    """
    Gets unique Labels (strings) from a pandas dataframe column and 
    replaces them by integers
    returns the converted dataframe and a dict with the
    label/number relationship
    """
    import numpy as np
    cat_labels = df[column].unique()
    cat_index = np.arange(0,len(cat_labels), 1)
    label_dict = dict(zip(cat_labels,cat_index))
    df_return = df.replace({column:label_dict})
    
    return df_return, label_dict



