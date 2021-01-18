import pandas as pd 
import numpy as np 
import sys
import os
import ast
from osgeo import gdal

#self-made functions
sys.path.append(os.path.realpath('../functions/'))
from findPixel import bruteForce
from findPixel import kwartetSearch
sys.path.append(os.path.realpath('../pandafy_data/'))

def addHeightBruteForce(folder="../../pandafied_data/", inputFile="tweetsWithTif.csv", saveFile='tweetsWithHeight.csv'):
    #load file
    tweets = pd.read_csv(folder + inputFile)
    heightTweet = []
    for i in range(len(tweets['latlon'])):
        latlon = ast.literal_eval(str(tweets['latlon'][i]))
        xPixel, yPixel = bruteForce(filename=tweets['tiffile'][i], lat=latlon[0], lon=latlon[1])

        filepath = '../../AHN2_5m/' + tweets['tiffile'][i]
        #print(filepath)
        dataset = gdal.Open(filepath, gdal.GA_ReadOnly) # Note GetRasterBand() takes band no. starting from 1 not 0
        width = dataset.RasterXSize
        height = dataset.RasterYSize
        band = dataset.GetRasterBand(1)
        arr = band.ReadAsArray()
        
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
        
        arr = arr[minX: maxX, minY:maxY]
        arr = arr.flatten()
        heightTweet.append(arr)
    tweets['height'] = heightTweet
    tweets.to_csv(folder+saveFile, index=False)
    print(tweets)

def addHeightKwartetSearch(folder="../../pandafied_data/", inputFile="tweetsWithTif.csv", saveFile='tweetsWithHeight.csv'):
    #load file
    tweets = pd.read_csv(folder + inputFile)
    
    # I had some trouble getting the dataframe dfArr to append to dfOffArr
    # This is because you cannot append to an empty dataframe
    # I could have chosen to find the dfArr of the first tweet and then do the rest
    # In this case I wanted to minimise the lines of code which is why I first add dfArr to a list
    # and then convert to a dataframe
    listOfArr = []
    dfOfArr = pd.DataFrame

    for i in range(len(tweets['latlon'])):
        # set parameter
        latlon = ast.literal_eval(str(tweets['latlon'][i]))
        
        # find pixel
        xPixel, yPixel = kwartetSearch(filename=tweets['tiffile'][i], lat=latlon[0], lon=latlon[1])

        # open tiff file
        filepath = '../../AHN2_5m/' + tweets['tiffile'][i]
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
    tweets=tweets.join(dfOfArr)
    tweets.to_csv(folder+saveFile, index=False)
    print(tweets)


if __name__ == '__main__':
    default = input('Default? y/n \n')
    if(default == 'n'):
        inputFile = input('Filename of input csv: \n')
        saveFile = input('Filename of savefile: \n')
        addHeightKwartetSearch(inputFile=inputFile, saveFile=saveFile)
    elif(default == 'y'):
        addHeightKwartetSearch()