import sys
import os
import pandas as pd 
import numpy as np 
from tqdm import tqdm
import ast
from osgeo import gdal

#self-made functions
sys.path.append(os.path.realpath('../functions/'))
from equalizeData import equalize_data
from findPixel import kwartetSearch
from filterTweets import filter_tweets

sys.path.append(os.path.realpath('../pandafy_data/'))

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

def addHeightKwartetSearch(data):
    print("Add height")
    # divide in positive and negative samples
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]

    print("total: "+ str(len(data)))
    print("positives: " + str(len(pos_data)))
    # I had some trouble getting the dataframe dfArr to append to dfOffArr
    # This is because you cannot append to an empty dataframe
    # I could have chosen to find the dfArr of the first tweet and then do the rest
    # In this case I wanted to minimise the lines of code which is why I first add dfArr to a list
    # and then convert to a dataframe
    listOfArr = []
    dfOfArr = pd.DataFrame

    for i in range(len(pos_data['latlon'])):
        # set parameter
        latlon = ast.literal_eval(str(pos_data['latlon'][i]))
        
        # find pixel
        xPixel, yPixel = kwartetSearch(filename=pos_data['tiffile'][i], lat=latlon[0], lon=latlon[1])

        # open tiff file
        filepath = '../../AHN2_5m/' + pos_data['tiffile'][i]
        dataset = gdal.Open(filepath, gdal.GA_ReadOnly) # Note GetRasterBand() takes band no. starting from 1 not 0
        width = dataset.RasterXSize
        height = dataset.RasterYSize
        band = dataset.GetRasterBand(1)
        arr = band.ReadAsArray()

        # If xPixel or yPixel is on the border, take a smaller square
        if xPixel -10 <= 0:
            minX = 1
        else:
            minX = xPixel-10
        
        if yPixel -10 <= 0:
            minY = 1
        else:
            minY = yPixel-10
        
        if xPixel +10 > width:
            xPixel = width
        else:
            maxX = xPixel +10

        if yPixel +10 > height:
            yPixel = height
        else:
            maxY = yPixel +10
        
        # find all values of the file within the square
        arr = arr[minX: maxX, minY:maxY]

        # convert to 1d array
        arr = arr.flatten()
        
        # convert to dataframe with the values being the columns
        dfArr = pd.DataFrame(arr)
        dfArr = dfArr.transpose()
        
        # add dataframe to list
        listOfArr.append(dfArr)
    
    # initialise with first element of list
    dfOfArr = listOfArr[0]
    # add all other elements of the list
    for tw in range(1,len(listOfArr)):
        dfOfArr=dfOfArr.append(listOfArr[tw], ignore_index=True)
    
    # join the height data with existing data and save
    data=pos_data.join(dfOfArr)
    data = data.append(neg_data)

    return(data)
    
def combineDataFrames(folder='../../pandafied_data/', rainFile = "pandafied_h5_rain_2017_12.csv", tweetFile="twitter_sample_tiff.csv", saveFile="labeledSample.csv"):
    #first load the data
    rain,tweets_XY = load_pandafied(folder=folder, rainFile=rainFile, tweetFile=tweetFile)
    #pick relevant columns from tweets_XY
    tweets_XY = tweets_XY.drop(columns=['time'])
    #remove duplicates
    tweets_XY = tweets_XY.drop_duplicates()
    
    #merge and label dataset
    rainTweets = pd.merge(rain, tweets_XY, on=('radarX','radarY','date'), how='left')
    rainTweets = make_labels(rainTweets,'text')
    
    #create sampleset with equal number of positive and negative examples
    #and filter out tweets without rain
    rainTweets_eq = equalize_data(data=rainTweets)
    rainTweets_eq = filter_tweets(data=rainTweets_eq, threshold=0)
    rainTweets_eq.to_csv("../../pandafied_data/raintweets_eq.csv", index=False)

    final = addHeightKwartetSearch(rainTweets_eq)

    #print and save
    print(final)
    final.to_csv(folder+saveFile, index=False)
    return final

if __name__ == '__main__':
    default = input("Default? y/n")
    if(default == "n"):
        rainFile=input("Enter file name of rain data:")
        tweetFile=input("Enter file name of twitter data:")
        saveFile=input("Enter name of save file:")
        combineDataFrames(rainFile=rainFile, tweetFile=tweetFile, saveFile=saveFile)
    elif(default == "y"):
        combineDataFrames()