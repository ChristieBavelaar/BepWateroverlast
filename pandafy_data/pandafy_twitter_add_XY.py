import pandas as pd
import numpy as np
import shapely
from shapely.geometry import Polygon,Point
import ast
from joblib import Parallel, delayed
import multiprocessing
import copy

def give_radarXY(df,radar,idx,total):
    df = copy.deepcopy(df)
    latlon = df['latlon'].values.tolist()[0]
    try:
        if np.isnan(latlon):
            df['radarX'] = [None]
            df['radarY'] = [None]
            return df
    except:
        pass
    try:
        latlon_point = ast.literal_eval(str(latlon))
        point = Point(latlon_point[1], latlon_point[0])
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
    except:
        df['radarX'] = [None]
        df['radarY'] = [None]
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

def pandafy_twitter_add_XY():
    tweets = pd.read_csv('../../pandafied_data/pandafied_twitter.csv')
    #radar = pd.read_csv('../../pandafied_data/pandafied_radar_coord.csv')
    radar = pd.read_csv('../../pandafied_data/pandafied_h5_radar.csv')
    tweets_XY = tweets_append_XY(tweets,radar)
    tweets_XY.to_csv('../../pandafied_data/pandafied_twitter_XY.csv',index=False)
    
def pandafy_curated_twitter_add_XY():
    tweets = pd.read_csv('../../pandafied_data/curated_twitter.csv')
    #radar = pd.read_csv('../../pandafied_data/pandafied_radar_coord.csv')
    radar = pd.read_csv('../../pandafied_data/pandafied_h5_radar.csv')
    tweets_XY = tweets_append_XY(tweets,radar)
    tweets_XY.to_csv('../../pandafied_data/curated_twitter_XY.csv',index=False)

def pandafy_twitter_2007_2020_add_XY(tweets_file_name='pandafied_twitter_2007-2020.csv',radar_file_name='pandafied_h5_radar.csv',save_name='pandafied_twitter_2007-2020_XY.csv'):
    '''
        This function reads the longitude latitude coordinate of each tweet and checks in which radar pixel it lies.
    '''
    #folder = '/data/s2155435/pandafied_data/'
    folder = '../../pandafied_data/'
    tweets = pd.read_csv(folder+tweets_file_name)
    radar = pd.read_csv(folder+radar_file_name)
    tweets_XY = tweets_append_XY(tweets,radar,folder+save_name)
    tweets_XY.to_csv(folder+save_name,index=False)

if __name__ == '__main__':
    pandafy_twitter_2007_2020_add_XY()
    
