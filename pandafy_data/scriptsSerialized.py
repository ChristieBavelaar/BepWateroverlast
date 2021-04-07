import pandas as pd
import sys
from pandafy_tiffs import pandafy_tiffs
from pandafy_twitter import pandafy_twitter
from pandafy_h5_make_radarXY import pandafy_h5_make_radarXY
from pandafy_twitter_add_XY import tweets_append_XY
from twitterSelect import selectTweets, selectSampleTweets
from KNMIRainSample import pandafy_h5
from pandafy_KNMI_rainFull import pandafy_h5_full
from addTifTwitter import tweets_append_tif
from combineData import combineDataFrames
from labelData import make_labels
from equalizeData import equalize_data
from seperateData import seperateData
from filterTweets import filter_tweets
from latlonTifNeg import addLatlonNegData
from addHeight import addHeightKwartetSearch
from recombinePosNeg import recombinePosNeg
from depSampling import dependent_sampling

if __name__ == '__main__':
    """From which step would like to start? (step 1-4 are not dependent) \n \
    1 give tiff files coordinates \n \
    2 pandafy twitter data \n \
    3 give radar XY coordinates \n \
    4 pandafy rain data \n \
    5 give tweets a radar XY \n \
    6 select tweets that apply to rain data \n \
    7 give each tweet a tif file \n \
    8 give each tweet a rain attribute \n \
    9 label the dataset \n \

    *** random sampling ***
    10 create equal number of positive and negative examples \n \
    (seperate the dataset into positive and negative examples) \n \
    11 filter positive examples below a rain threshold \n \
    12 give negative examples latlon and tif file \n \
    (recombine positive and negative examples) \n \
    13 add height attributes to examples\n \
    14 equalize the data again 

    *** dependant sampling ***
    (seperate the dateset into positive and negative examples)
    11 filter positive examples below a rain threshold
    15 equalize dataset with dependant sampling
    (recombine positive and negative examples)
    13 add height attributes to examples

    sys.argv[1] = sample
    sys.argv[2] = start"""
    folder = "/data/s2155435/pandafied_data/"
    savefile = "labeledSample_eq.csv"


    sample = sys.argv[1]
    start = int(sys.argv[2])
    
    if(sample == 'y'):
        samplename = 'Sample'
        folder = '../../pandafied_data/'
    else:
        samplename = ''
    
    # Files that have to be accessed by multiple steps
    if start>0:
        if start <= 4 or start == 6:
            latlonTif = pd.read_csv(folder+"lat_lon_to_filename.csv") #5

        if start <= 6 or start == 8:
            if sample == 'y':
                rain = pd.read_csv(folder+"pandafied_h5_rain_2017_12.csv") #7
            else:
                rain = pd.read_csv(folder+"pandafied_h5_rain_2007-2020.csv")

        if start == 1 or start == 3:
            radar = pd.read_csv(folder+"pandafied_h5_radar.csv") #2

        if start == 2 or start == 3:
            tweets = pd.read_csv(folder+"pandafied_twitter_2007-2020.csv") #1
            future = 3

        if start == 5 or start == 6:
            if sample == 'y':
                data = pd.read_csv(folder+"pandafied_twitter_2017_12.csv")
            else:
                data = pd.read_csv(folder+"twitter_2010-2017_XY.csv") #4
            future = 6

        if start == 7 or start == 8:
            if sample == 'y':
                data = pd.read_csv(folder+"twitter_sample_tiff.csv") #6
            else:
                data = pd.read_csv(folder+"twitter_2010-2017_XY_tiff.csv")
            future = 8

        if start == 11 or start == 12:
            posData = pd.read_csv(folder+"posData" + samplename+ ".csv") #10
            negData = pd.read_csv(folder+"negData" + samplename +".csv") #10

    # Files only to be accessed by one step
    if start == 0:
        tweets = pandafy_twitter()
        radar = pandafy_h5_make_radarXY()
        latlonTif = pandafy_tiffs() #5
        if sample == 'y':
            rain = pandafy_h5()
        else:
            rain = pandafy_h5_full()
        future = 3

    elif start == 1:
        tweets = pandafy_twitter() #1
        future = 3
    
    elif start == 2:
        radar = pandafy_h5_make_radarXY() #2

    elif start == 4:
        data = pd.read_csv(folder+"pandafied_twitter_2007-2020_XY.csv") #3
        future = 4
    
    elif start == 5:
        latlonTif = pandafy_tiffs() #5
    
    elif start == 7:
        if sample == 'y':
            rain = pandafy_h5()
        else:
            rain = pandafy_h5_full()
    
    elif start == 9:
        data = pd.read_csv(folder+"combinedData"+samplename +".csv") #8
        future = 9
    
    elif start == 10:
        data = pd.read_csv(folder+"labeledData"+samplename +".csv") #9
        future = 10
    
    elif start == 11:
        negData = pd.read_csv(folder+'latlonTifNeg'+samplename+'.csv')
        future = 11
    
    elif start == 12:
        posData = pd.read_csv(folder+'filteredTweets'+samplename+'.csv')
        future = 12
    
    elif start == 13:
        data = pd.read_csv(folder+"recombinedData" +samplename +".csv")
        future = 13
    
    elif start == 14:
        data = pd.read_csv(folder+"heightData"+samplename+".csv") #15
        future = 14
    
    elif start == 15:
        data = pd.read_csv(folder+"labeledData"+samplename +".csv") #9
        future = 15

    # perform al steps in sequence
    if future == 3:
        savename = 'pandafied_twitter_2007-2020_XY.csv'
        data = tweets_append_XY(tweets,radar, folder+savename)
        future = 4

    if future == 4:
        if sample == 'y':
            data = selectSampleTweets(data, folder+'pandafied_twitter_2017_12.csv')
        else:
            data = selectTweets(data, folder + 'twitter_2010-2017_XY.csv')
        future = 6

    if future == 6:
        if sample == 'y':
            savename = 'twitter_sample_tiff.csv'
        else:
            savename = 'twitter_2010-2017_XY_tiff.csv'
        data = tweets_append_tif(data, latlonTif, folder+savename)
        future = 8

    if future == 8:
        data = combineDataFrames(data, rain, folder+'combinedData'+samplename+'.csv')
        future = 9

    if future == 9:
        data = make_labels(data, 'text', folder+'labeledData'+samplename+'.csv')
        future = 10
    
    if future == 10:
        data = equalize_data(data, folder+'equalizedData'+samplename+'.csv')
        posData, negData = seperateData(data, folder+'posData'+samplename+'.csv', folder+'negData'+samplename+'.csv')
        posData = filter_tweets(posData,10, folder+'filteredTweets'+samplename+'.csv')
        negData = addLatlonNegData(negData, folder+'latlonTifNeg'+samplename+'.csv')
        future =12.5
    
    if future == 11:
        posData = filter_tweets(posData,10, folder+'filteredTweets'+samplename+'.csv')
        future = 13

    if future == 12:
        negData = addLatlonNegData(negData, folder+'latlonTifNeg'+samplename+'.csv')
        future = 12.5

    if future == 12.5:
        data = recombinePosNeg(posData, negData, folder+'recombinedData'+samplename+'.csv')
        future = 13
    
    if future == 13:
        data = addHeightKwartetSearch(data, folder+'heightData'+samplename+'.csv')
        future = 14

    if future == 14:
        data = equalize_data(data, folder+'finalData'+samplename+'.csv')
    
    if future == 15:
        posData, negData = seperateData(data, folder+'posData'+samplename+'.csv', folder+'negData'+samplename+'.csv')
        posData = filter_tweets(posData,10, folder+'filteredTweets'+samplename+'.csv')
        posData, negData = dependent_sampling(posData, negData, folder+"posDep"+samplename+'.csv', folder+'negDep'+samplename+'.csv')
        posData = addHeightKwartetSearch(posData, folder+"posHeight"+samplename+'.csv')
        negData = addHeightKwartetSearch(negData, folder+"negHeight"+samplename+'.csv')
        print(posData)
        print(negData)