import pandas as pd
from pandafy_tiffs import pandafy_tiffs
from pandafy_twitter import pandafy_twitter
from pandafy_h5_make_radarXY import pandafy_h5_make_radarXY
from pandafy_twitter_add_XY import tweets_append_XY
from twitterSelect import selectTweets, selectSampleTweets
from KNMIRainSample import pandafy_h5
from addTifTwitter import tweets_append_tif
from combineData import combineDataFrames
from labelData import make_labels
from equalizeData import equalize_data
from seperateData import seperateData
from filterTweets import filter_tweets
from latlonTifNeg import addLatlonNegData
from addHeight import addHeightKwartetSearch
from recombinePosNeg import recombinePosNeg

if __name__ == '__main__':
    folder = "../../pandafied_data/"
    try: 
        latlonTif = pd.read_csv(folder+"lat_lon_to_filename.csv")
    except:
        latlonTif = pandafy_tiffs()
    
    try:
        tweets = pd.read_csv(folder+"pandafied_twitter_2007-2020.csv")
    except:
        tweets = pandafy_twitter()
    
    try: 
        radar = pd.read_csv(folder+"pandafied_h5_radar.csv")
    except:
        radar = pandafy_h5_make_radarXY()
    
    try:
        rain = pd.read_csv(folder+"pandafied_h5_rain_2017_12.csv")
    except:
        rain = pandafy_h5()
    
    try:
        data = pd.read_csv(folder+'pandafied_twitter_2007-2020_XY.csv')
    except:
        tweets_append_XY(tweets, radar)

    commands1 = [selectSampleTweets(data), tweets_append_tif(data, latlonTif), combineDataFrames(data, rain), make_labels(data, 'text'), equalize(data)]

    for i in rang(len(commands1)):
        print(str(commands[1]))
        data = commands1[i]
        data.to_csv(folder+i+".csv") 
    
    posData, negData = seperate(data)
    posData = filter_tweets(posData)
    negData = addLatlonNegData(negData)

    commands2 = [recombinePosNeg(posData, negData), addHeightKwartetSearch(data), equalize_data(data)]
    
    for j in range(i,len(commands2)+i):
        data = commands2[j]
        data.to_csv(folder+j+".csv")
    