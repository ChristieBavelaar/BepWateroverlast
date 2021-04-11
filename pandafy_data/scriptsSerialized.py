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
from adresSampling import adress_sampling

if __name__ == '__main__':
    """
    From which step would like to start? (step 1-4 are not dependent) \n \
    1 give tiff files coordinates \n \
    2 pandafy twitter data \n \
    3 give radar XY coordinates \n \
    4 pandafy rain data \n \
    5 give tweets a radar XY \n \
    6 select tweets that apply to rain data \n \
    7 give each tweet a tif file \n \
    8 give each tweet a rain attribute \n \
    9 label the dataset \n \
    10 filter data below treshold

    11 Sampling
        *** random sampling ***
        - equalize random \n \
        - seperate the dataset into positive and negative examples) \n \
        - give negative examples latlon and tif file \n \
        - recombine positive and negative examples \n \
        - add height attributes to examples\n \
        - equalize the data again 

        *** address sampling ***
        - equalize dataset with address sampling
        - add height attributes to examples
        - equalize the data again

        *** dependant sampling ***
        - seperate the dateset into positive and negative examples
        - equalize dataset with dependant sampling
        - add height attributes to examples

    sys.argv[1] = sample y/n
    sys.argv[2] = start [1,11]
    sys.arg[3] = sampling method
                    1 : random
                    2 : adress
                    3 : dependent

    sys.argv[4] = rain threshold
    """

    folder = "/data/s2155435/pandafied_data/"

    sample = sys.argv[1]
    start = int(sys.argv[2])
    sampMethod = int(sys.argv[3])
    threshold = int(sys.argv[4])

    if(sample == 'y'):
        samplename = 'Sample'
        folder = '../../pandafied_data/'
        alice = False
    else:
        samplename = ''
        folder = "/data/s2155435/pandafied_data/"
        alice = True
    
    # Files that have to be accessed by multiple steps
    if start>0:
        if start <= 4 or start == 6 or sampMethod == 2:
            latlonTif = pd.read_csv(folder+"lat_lon_to_filename.csv") #5

        if start <= 6 or start == 8:
            if sample == 'y':
                rain = pd.read_csv(folder+"pandafied_h5_rain_2017_12.csv") #7
            else:
                rain = pd.read_csv(folder+"pandafied_h5_rain_2007-2020.csv")

        if start == 1 or start == 3 or sampMethod == 2:
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
        data = pd.read_csv(folder+'filteredData'+samplename+'.csv') #9
        future = 11

    if sampMethod == 2:
        adresses = pd.read_csv(folder+"verblijfplaatsen.csv")

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
    
    if future == 10: # filter data below threshold
        data = filter_tweets(data, threshold, folder+'filteredData'+samplename+'.csv')
        future = 11

    if future == 11:
        print("start sampling with method ", sampMethod)
        if sampMethod <= 2:
            if sampMethod == 1:
                print(data)
                data = equalize_data(data, folder+'equalizedData'+samplename+'.csv', extra=2)
                posData, negData = seperateData(data, folder+'posData'+samplename+'.csv', folder+'negData'+samplename+'.csv')
                negData = addLatlonNegData(negData, folder+'latlonTifNeg'+samplename+'.csv',alice)
                data = recombinePosNeg(posData, negData, folder+'recombinedData'+samplename+'.csv')
                #print(data)
            else:
                data = adress_sampling(data, adresses, latlonTif, radar, folder+'recombinedData'+samplename+'csv')
            data = addHeightKwartetSearch(data, folder+'heightData'+samplename+'.csv',alice)
            #print(data)
            data = equalize_data(data, folder+'finalData'+samplename+'.csv')
        else: 
            posData, negData = seperateData(data, folder+'posData'+samplename+'.csv', folder+'negData'+samplename+'.csv')
            posData, negData = dependent_sampling(posData, negData, folder+"posDep"+samplename+'.csv', folder+'negDep'+samplename+'.csv')
            posData = addHeightKwartetSearch(posData, folder+"posHeight"+samplename+'.csv',alice)
            negData = addHeightKwartetSearch(negData, folder+"negHeight"+samplename+'.csv', alice)
    
