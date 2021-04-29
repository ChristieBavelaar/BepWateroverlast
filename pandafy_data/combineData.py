import pandas as pd 

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
    #folder = "../../pandafied_data/"
    folder = "/data/s2155435/pandafied_data"

    print("Load data")
    tweets_XY = pd.read_csv(folder + tweetFile)
    rain = pd.read_csv(folder + rainFile)

    combinedData = combineDataFrames(tweets_XY, rain, folder+saveFile)