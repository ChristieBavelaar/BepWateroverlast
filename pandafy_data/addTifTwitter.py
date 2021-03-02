import pandas as pd 
import sys
import os

#self-made functions
sys.path.append(os.path.realpath('../tifFiles/'))
from getTif import determineTifFile
sys.path.append(os.path.realpath('../pandafy_data/'))

import pandas as pd
import numpy as np
import shapely
from shapely.geometry import Polygon,Point
import ast
from joblib import Parallel, delayed
import multiprocessing
import copy

def add_filename(df,tif,idx,total):
    df = copy.deepcopy(df)
    print(idx,total)
    latlon = df['latlon'].values.tolist()[0]

    # Soms is een deel van het twitter bericht in de colom latlon terecht gekomen. 
    # Probeer de waarde van latlon om te zetten naar een punt
    # Als dit niet lukt is de waarde een deel van het twitter bericht
    # Sla de gehele rij over, deze komt niet in de output
    try:
        latlon_point = ast.literal_eval(str(latlon))
        point = Point(latlon_point[1], latlon_point[0])
        for i in range(len(tif['latlon_sw'])):
            sw = ast.literal_eval(str(tif['latlon_sw'][i]))
            se = ast.literal_eval(str(tif['latlon_se'][i]))
            ne = ast.literal_eval(str(tif['latlon_ne'][i]))
            nw = ast.literal_eval(str(tif['latlon_nw'][i]))
            polygon = Polygon(((sw[1], sw[0]), (se[1], se[0]), (ne[1], ne[0]), (nw[1], nw[0]), (sw[1], sw[0])))
            if(polygon.contains(point)):
                df['tiffile'] = [tif['file_name'][i]]
                return df
    except:
        print("exception occured")
    return 

def tweets_append_tif(tweets,tif):
    num_cores = multiprocessing.cpu_count()
    print("num_cores: " + str(num_cores))
    
    results = Parallel(n_jobs=num_cores)(delayed(add_filename)(tweets[i:i+1],tif,i,len(tweets.index)) for i in tweets.index)

    tweets_tif = pd.DataFrame({})
    for i in results:
        tweets_tif = tweets_tif.append(i)

    return tweets_tif

if __name__ == '__main__':
    default = input("Sample? y/n \n")
    if(default == "n"):
        saveFile= "twitter_2010-2017_XY_tiff.csv"
        tweets= pd.read_csv("../../pandafied_data/twitter_2010-2017_XY.csv")
        tif= pd.read_csv('../../pandafied_data/lat_lon_to_filename.csv')
    elif(default == "y"):
        tweets= pd.read_csv('../../pandafied_data/pandafied_twitter_2017_12.csv')
        tif= pd.read_csv('../../pandafied_data/lat_lon_to_filename.csv')
        saveFile='twitter_sample_tiff.csv'
    else:
        tweets= pd.read_csv('../../pandafied_data/negatives.csv')
        tif= pd.read_csv('../../pandafied_data/lat_lon_to_filename.csv')
        saveFile='negativesTiff.csv'
    tweets_tif=tweets_append_tif(tweets=tweets, tif=tif)
    tweets_tif.to_csv('../../pandafied_data/'+saveFile, index=False)
