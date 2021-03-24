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
    tweets_XY = tweets_XY.drop(columns=['time'])
    #remove duplicates
    tweets_XY = tweets_XY.drop_duplicates()
    
    rain['date'] = rain['date'].astype('object')
    print("Merge data")
    rainTweets = pd.merge(rain, tweets_XY, on=('radarX','radarY','date'), how='left')

    rainTweets.to_csv(saveFile, index=False)
    return rainTweets

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        rainFile="pandafied_h5_rain_2017_12.csv"
        tweetFile= "twitter_sample_tiff.csv" 
        saveFile="combinedDataSample.csv"
    elif(sample == "n"):
        rainFile="pandafied_h5_rain_2007-2020.csv"
        tweetFile= "twitter_2010-2017_XY.csv"
        saveFile="combinedData.csv"
    
    folder = "../../pandafied_data/"

    print("Load data")
    tweets_XY = pd.read_csv(folder + tweetFile)
    rain = pd.read_csv(folder + rainFile)

    combinedData = combineDataFrames(tweets_XY, rain, folder+saveFile)