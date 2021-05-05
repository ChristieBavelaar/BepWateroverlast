import pandas as pd
import numpy as np
import shapely
from shapely.geometry import Polygon,Point
import ast
from joblib import Parallel, delayed
import multiprocessing
import copy

def give_radarXY(df,radar,idx,total):
    print(idx, '/', total)

    lat = df['latitude'].values.tolist()[0]
    lon = df['longitude'].values.tolist()[0]
    point = Point(lon,lat)

    for i in range(len(radar['latlon_sw'])):
        sw = ast.literal_eval(str(radar['latlon_sw'][i]))
        se = ast.literal_eval(str(radar['latlon_se'][i]))
        ne = ast.literal_eval(str(radar['latlon_ne'][i]))
        nw = ast.literal_eval(str(radar['latlon_nw'][i]))
        polygon = Polygon(((sw[1], sw[0]), (se[1], se[0]), (ne[1], ne[0]), (nw[1], nw[0]), (sw[1], sw[0])))
        if(polygon.contains(point)):
            df['radarX'] = [radar['radarX'][i]]
            df['radarY'] = [radar['radarY'][i]]
            return df

    return df

def tweets_append_XY(tweets,radar, saveFile):
    print(tweets)
    num_cores = multiprocessing.cpu_count()
    print("num_cores: " + str(num_cores))
    results = Parallel(n_jobs=num_cores)(delayed(give_radarXY)(tweets[i:i+1],radar,i,len(tweets.index)) for i in tweets.index)
    tweets_XY = pd.DataFrame({})
    for i in results:
        tweets_XY = tweets_XY.append(i)
    
    # Delete unnamed columns
    cols = [col for col in tweets_XY.columns if 'Unnamed' not in col]
    tweets_XY = tweets_XY[cols]

    tweets_XY.to_csv(saveFile, index=False)
    return tweets_XY

if __name__ == '__main__':
    # folder = "../../csv112/"    
    # radar = pd.read_csv(folder+'pandafied_h5_radar.csv')
    # pd112 = pd.read_csv(folder+'112RelevantSample.csv')
    # output = tweets_append_XY(tweets=pd112, radar=radar, saveFile=folder+'112XYSample.csv')
    
    folder = "/data/s2155435/csv112/"    
    radar = pd.read_csv(folder+'pandafied_h5_radar.csv')
    pd112 = pd.read_csv(folder+'112Relevant.csv')
    output = tweets_append_XY(tweets=pd112, radar=radar, saveFile=folder+'112XY.csv')
    
