import pandas as pd 
import numpy as np

def combineDataFrames1(tweets_XY, rain, saveFile):
    """
        Merge twitter and rain data into one dataframe.
        Parameters: 
            tweets_XY: pandas dataframe containing twitter messages
            rain: pandas dataframe containing rain data
        Output: pandas dataframe
        Source: Christiaan
    """

    print("Preprocess tweets")
    #pick relevant columns from tweets_XY
    tweets_XY['dateh'] = tweets_XY['time'].astype(str).str.slice(0,10).astype('object')
    tweets_XY = tweets_XY.drop(columns=['time','date'])

    #remove duplicates
    tweets_XY = tweets_XY.drop_duplicates()
    
    rain=rain.drop(columns='date')
    rain = rain[rain['dateh'].notnull()]
    rain['dateh'] = rain['dateh'].astype('object')
    
    rain = rain.reset_index(drop=True)

    print("Merge data")
    print(tweets_XY)
    print(rain)
    rainTweets = pd.merge(rain, tweets_XY, on=('radarX','radarY','dateh'), how='left')
    rainTweets=rainTweets[rainTweets['rain'].notnull()]
    rain = rain.reset_index(drop=True)
    
    rainTweets.to_csv(saveFile, index=False)
    return rainTweets

def combineDataFrames(tweets_XY, rain, saveFile):
    """
        Merge twitter and rain data into one dataframe.
        Parameters: 
            tweets_XY: pandas dataframe containing twitter messages
            rain: pandas dataframe containing rain data
        Output: pandas dataframe
        Source: Christiaan
    """

    print("Preprocess tweets")
    #pick relevant columns from tweets_XY
    tweets_XY['date'] = tweets_XY['date'].astype('object')
    tweets_XY = tweets_XY.drop(columns=['time'])

    #remove duplicates
    tweets_XY = tweets_XY.drop_duplicates()
    
    rain = rain[rain['date'].notnull()]
    rain['date'] = rain['date'].astype('object')
    
    rain = rain.reset_index(drop=True)

    print("Merge data")
    print(tweets_XY)
    print(rain)
    rainTweets = pd.merge(rain, tweets_XY, on=('radarX','radarY','date'), how='left')
    rainTweets=rainTweets[rainTweets['rain'].notnull()]
    rain = rain.reset_index(drop=True)
    
    rainTweets.to_csv(saveFile, index=False)
    return rainTweets
    
def rainAttributes(tweets_XY, rain, saveFile, nrHours):
    print("Preprocess tweets")
    tweets_XY['date'] = tweets_XY['date'].astype('object')
    tweets_XY['hour'] = tweets_XY['time'].astype(str).str.slice(8,10).astype(int)
    
    print('Preprocess rain')
    rain['date']= pd.to_datetime(rain['date'], format='%Y%m%d')
    #rain['hour']=rain['hour'].astype(int)
    # rain['date'] = rain['dateh'].astype(str).str.slice(0,8).astype('object')
    # print('step1')
    # rain['hour'] = rain['dateh'].astype(str).str.slice(8,10).astype(int)
    
    totalData = pd.DataFrame()
    print(tweets_XY,rain.dtypes)
    dayRain = []
    pastRain = []
    for i in range(len(tweets_XY.index)):
        day = pd.to_datetime(tweets_XY.iloc[i]['date'], format='%Y%m%d')
        dayData = rain[(rain['date']==day) & (rain['radarY']==tweets_XY.iloc[i]['radarY']) & (rain['radarX']==tweets_XY.iloc[i]['radarX'])]
        npDay = dayData.to_numpy()
        dayRain.append(npDay[0,0])
        if nrHours > tweets_XY.iloc[i]['hour']:
            npDay = npDay[0,4:tweets_XY.iloc[i]['hour']+1]
            prevday = day - pd.Timedelta('1 days')
            prevDayData = rain[(rain['date']==prevday) & (rain['radarY']==tweets_XY.iloc[i]['radarY']) & (rain['radarX']==tweets_XY.iloc[i]['radarX'])]
            npPrevday = prevDayData.to_numpy()
            npPrevday = npPrevday[0, 4+(23 - (nrHours - tweets_XY.iloc[i]['hour'])):]

            totalPastRain = np.concatenate((npPrevday,npDay)).sum()
            pastRain.append(totalPastRain)
        else:
            npDay = npDay[0,4:nrHours+1].sum()
            pastRain.append(npDay)
    tweets_XY['rain'] = dayRain
    tweets_XY['rain'+str(nrHours)] = pastRain
 
    print(tweets_XY)
        

if __name__ == '__main__':
    # sample = input("Sample? y/n")
    # if(sample == "y"):
    #     rainFile="pandafied_h5_rain_2017_12.csv"
    #     tweetFile= "twitter_sample_tiff.csv" 
    #     saveFile="combinedDataSample.csv"
    # elif(sample == "n"):
    #     rainFile="pandafied_h5_rain_2007-2020.csv"
    #     tweetFile= "twitter_2010-2017_XY.csv"
    #     saveFile="combinedData.csv"
    rainFile="pandafied_h5_rain_2017_12.csv"
    tweetFile= "twitter_sample_tiff.csv" 
    saveFile="combinedDataSample.csv"
    folder = "../../pandafied_data/"
    #folder = "/data/s2155435/pandafied_data/"

    print("Load data")
    tweets_XY = pd.read_csv(folder + tweetFile)
    rain = pd.read_csv(folder + rainFile)

    Output=rainAttributes(tweets_XY,rain,folder+saveFile,12)
    #combinedData = combineDataFrames(tweets_XY, rain, folder+saveFile)