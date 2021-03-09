import sys
import os
import pandas as pd 
import numpy as np 
from tqdm import tqdm
import ast
from osgeo import gdal
import shapely
from shapely.geometry import Polygon,Point
import random
#self-made functions
sys.path.append(os.path.realpath('../functions/'))
from equalizeData import equalize_data
from findPixel import kwartetSearch
from filterTweets import filter_tweets
sys.path.append(os.path.realpath('../pandafy_data/'))
from addTifTwitter import tweets_append_tif


sys.path.append(os.path.realpath('../pandafy_data/'))

def load_pandafied(folder='../../pandafied_data/', rainFile = "pandafied_h5_rain_2017_12.csv", tweetFile="pandafied_twitter_2017_12.csv", radarFile="pandafied_h5_radar.csv"):
    print("load rain data")
    rain = pd.read_csv(folder + rainFile)
    print("load tweets")
    tweets_XY = pd.read_csv(folder + tweetFile)
    print("load radar")
    radar = pd.read_csv(folder+radarFile)
    return rain, tweets_XY, radar
    
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

def addLatlonNegData(data, radar):
    tif= pd.read_csv('../../pandafied_data/lat_lon_to_filename.csv')

     # divide in positive and negative samples
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]
    
    neg_data = pd.merge(neg_data, radar, on=('radarX','radarY'), how='left')
    
    print("total: "+ str(len(data)))
    print("positives: " + str(len(pos_data)))

    for i in range(len(neg_data['latlon_sw'])):
        sw = ast.literal_eval(str(neg_data['latlon_sw'][i]))
        se = ast.literal_eval(str(neg_data['latlon_se'][i]))
        ne = ast.literal_eval(str(neg_data['latlon_ne'][i]))
        nw = ast.literal_eval(str(neg_data['latlon_nw'][i]))

        polygon = Polygon(((sw[1], sw[0]), (se[1], se[0]), (ne[1], ne[0]), (nw[1], nw[0]), (sw[1], sw[0])))
        min_x, min_y, max_x, max_y = polygon.bounds
        
        while True:
            randomPoint = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
            if(polygon.contains(randomPoint)):
                neg_data['latlon'][i] = "("+str(randomPoint.y)+","+str(randomPoint.x)+")"
                # print("types")
                # print("randomPoint: ", type(randomPoint))
                # print("randomPoint coords: ", type(randomPoint.coords))
                # print("randomPoint.x: ", type(randomPoint.x))
                # print("tupel: ", type(neg_data['latlon'][i]))
                # print("tiffile: ", neg_data['tiffile'][i])
                # #xPixel, yPixel = kwartetSearch(filename=neg_data['tiffile'][i], lat=randomPoint.x, lon=randomPoint.y)
                break
    #neg_data['latlon'] = neg_data['latlon_center']
    neg_data.to_csv("../../pandafied_data/negatives.csv", index=False)
    print("add tiff files to negative examples")
    neg_data = tweets_append_tif(neg_data, tif)
    neg_data.to_csv("../../pandafied_data/negatives2.csv", index=False)

    neg_data = neg_data.drop(columns=['latlon_center','latlon_ne',"latlon_nw", 'latlon_se', 'latlon_sw'])
    data = pos_data.append(neg_data, ignore_index = True)
    #print("total:",type(data['latlon']))
    return data

def addHeightKwartetSearch(data, radar):
    print("Add height")

    data = addLatlonNegData(data,radar)
    # I had some trouble getting the dataframe dfArr to append to dfOffArr
    # This is because you cannot append to an empty dataframe
    # I could have chosen to find the dfArr of the first tweet and then do the rest
    # In this case I wanted to minimise the lines of code which is why I first add dfArr to a list
    # and then convert to a dataframe
    listOfArr = []
    dfOfArr = pd.DataFrame
    #print(data)
    for i in range(len(data['latlon'])):
        #print(data.loc[[i]])
        #print("data['latlon'][i]", type(data['latlon'][i]))

        try:
            #print("data['latlon'][i]", type(data['latlon'][i]))
            # set parameter
            latlon = ast.literal_eval(str(data['latlon'][i]))
            #print("latlon", type(latlon))
            #print("doorgeven van ", latlon[0])
            #print("latlon[0]", type(latlon[0]))
            # find pixel
            xPixel, yPixel = kwartetSearch(filename=data['tiffile'][i], lat=latlon[0], lon=latlon[1])
            print("location",i, ": ", xPixel, yPixel)
        except:
            print("went wrong")
            break
            #print(data['latlon'][i].values)
            #latlon[0], latlon[1] = data['latlon'][i].split(",")
            #xPixel, yPixel = kwartetSearch(filename=data['tiffile'][i], lat=latlon[0], lon=latlon[1])

        # open tiff file
        filepath = '../../AHN2_5m/' + data['tiffile'][i]
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
    data=data.join(dfOfArr)
    #print(data)
    return(data)
    
def combineDataFrames(folder='../../pandafied_data/', rainFile = "pandafied_h5_rain_2007-2020.csv", tweetFile="twitter_2010-2017_XY_tiff.csv", saveFile="labeledData_eq.csv", radarFile="pandafied_h5_radar.csv"):
    #first load the data
    rain,tweets_XY,radar = load_pandafied(folder=folder, rainFile=rainFile, tweetFile=tweetFile, radarFile=radarFile)
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

    #find latlon coordiantes for negative examples
    rainTweets_eq = addLatlonNegData(data=rainTweets_eq, radar=radar)

    #Add the heigth
    final = addHeightKwartetSearch(rainTweets_eq, radar)
    #final = rainTweets_eq

    #print and save
    print(final)
    final.to_csv(folder+saveFile, index=False)
    return final

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        rainFile="pandafied_h5_rain_2017_12.csv"
        tweetFile= "twitter_sample_tiff.csv"
        saveFile="labeledSample_eq.csv"
        combineDataFrames(rainFile=rainFile, tweetFile=tweetFile, saveFile=saveFile)
    elif(sample == "n"):
        combineDataFrames()