# 4 add tiffile
import pandas as pd
import numpy as np
import shapely
from shapely.geometry import Polygon,Point
import ast
from joblib import Parallel, delayed
import multiprocessing
import copy

def determineTifFile(lat, lon, folder='/data/s2155435/pandafied_data/', file="lat_lon_to_filename.csv"):
    data=pd.read_csv(folder + file)
    point = Point(lon,lat)
    for i in range(len(data['latlon_sw'])):
        sw = ast.literal_eval(str(data['latlon_sw'][i]))
        se = ast.literal_eval(str(data['latlon_se'][i]))
        ne = ast.literal_eval(str(data['latlon_ne'][i]))
        nw = ast.literal_eval(str(data['latlon_nw'][i]))
        polygon = Polygon(((sw[1], sw[0]), (se[1], se[0]), (ne[1], ne[0]), (nw[1], nw[0]), (sw[1], sw[0])))
        if(polygon.contains(point)):
            return data['file_name'][i]

def add_filename(df,tif,idx,total):
    print(idx,total)
    lat = df['latitude'].values.tolist()[0]
    lon = df['longitude'].values.tolist()[0]
    point = Point(lon,lat)
    # Soms is een deel van het twitter bericht in de colom latlon terecht gekomen. 
    # Probeer de waarde van latlon om te zetten naar een punt
    # Als dit niet lukt is de waarde een deel van het twitter bericht
    # Sla de gehele rij over, deze komt niet in de output
    try:
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

def tweets_append_tif(tweets,tif, saveFile):
    print("Find tif-files")
    
    num_cores = multiprocessing.cpu_count()
    print("num_cores: " + str(num_cores))
    
    results = Parallel(n_jobs=num_cores)(delayed(add_filename)(tweets[i:i+1],tif,i,len(tweets.index)) for i in tweets.index)

    tweets_tif = pd.DataFrame({})
    for i in results:
        tweets_tif = tweets_tif.append(i)

    tweets_tif.to_csv(saveFile, index=False)
    return tweets_tif

if __name__ == '__main__':
    folder = '../../csv112/'
    tif = pd.read_csv(folder+'lat_lon_to_filename.csv')
    # pdRandom = pd.read_csv(folder+'randomSampledSample.csv')
    # pdAdress = pd.read_csv(folder +'adressSampledSample.csv')
    # pdDep = pd.read_csv(folder+'112LabeledSample.csv')
    pdDep2 = pd.read_csv(folder+'112DayRainSample.csv')

    # outputRandom = tweets_append_tif(tweets=pdRandom, tif=tif, saveFile=folder+'randomTifSample.csv')
    # print(outputRandom)

    # outputAdress = tweets_append_tif(tweets=pdAdress, tif=tif, saveFile=folder+'adressTifSample.csv')
    # print(outputAdress) 

    # outputDep = tweets_append_tif(tweets=pdDep, tif=tif, saveFile=folder+'depTifSample.csv')
    # print(outputDep)

    outputDep2 = tweets_append_tif(tweets=pdDep2, tif=tif, saveFile=folder+'112TifSample.csv')
    print(outputDep2)
