import pandas as pd 
import numpy as np 
from tqdm import tqdm

def load_pandafied(folder='../../pandafied_data/', rainFile = "pandafied_h5_rain_2017_12.csv", tweetFile="pandafied_twitter_2017_12.csv"):
    print("load rain data")
    rain = pd.read_csv(folder + rainFile)
    print("load tweets")
    tweets_XY = pd.read_csv(folder + tweetFile)
    return rain, tweets_XY
    
def make_labels(data,label_on):
    labels = []
    print("make_labels:")
    for i in tqdm(data[label_on]):
        try:
            if np.isnan(i):
                num=0
            else:
                num=1
        except:
            num=1
        labels.append(num)
    data['labels'] = labels
    return data

def combineDataFrames(folder='../../pandafied_data/', rainFile = "pandafied_h5_rain_2017_12.csv", tweetFile="tweetsWithHeight.csv", saveFile="labeledSample.csv"):
    #first load the data
    rain,tweets_XY = load_pandafied(folder=folder, rainFile=rainFile, tweetFile=tweetFile)
    #pick relevant columns from tweets_XY
    tweets_XY = tweets_XY.drop(columns=['latlon', 'time'])
    #remove duplicates
    tweets_XY = tweets_XY.drop_duplicates()
    print(tweets_XY)

    #merge and label dataset
    rainTweets = pd.merge(rain, tweets_XY, on=('radarX','radarY','date'), how='left')
    print(rainTweets)
    rainTweets = make_labels(rainTweets,'text')
    print(rainTweets)
    #print and save
    #print(rainTweets)
    rainTweets.to_csv(folder+saveFile, index=False)
    return rainTweets

if __name__ == '__main__':
    default = input("Default? y/n")
    if(default == "n"):
        rainFile=input("Enter file name of rain data:")
        tweetFile=input("Enter file name of twitter data:")
        saveFile=input("Enter name of save file:")
        combineDataFrames(rainFile=rainFile, tweetFile=tweetFile, saveFile=saveFile)
    elif(default == "y"):
        combineDataFrames()