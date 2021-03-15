import pandas as pd
from osgeo import gdal 
import sys
import os
#import numpy as np 
import ast
import shapely
import shapely
from shapely.geometry import Polygon,Point
import random
from addTifTwitter import tweets_append_tif

sys.path.append(os.path.realpath('../functions/'))
from findPixel import kwartetSearch

def addHeightKwartetSearch(data):
    print("Add height")

    print("Load radar data")
    radar = pd.read_csv('../../pandafied_data/pandafied_h5_radar.csv')

    # I had some trouble getting the dataframe dfArr to append to dfOffArr
    # This is because you cannot append to an empty dataframe
    # I could have chosen to find the dfArr of the first tweet and then do the rest
    # In this case I wanted to minimise the lines of code which is why I first add dfArr to a list
    # and then convert to a dataframe
    
    listOfArr = []
    dfOfArr = pd.DataFrame

    for i in range(len(data['latlon'])):
        try:
            latlon = ast.literal_eval(str(data['latlon'][i]))

            #find pixel
            xPixel, yPixel = kwartetSearch(filename=data['tiffile'][i], lat=latlon[0], lon=latlon[1])
        except:
            print("An exception occured")

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

    return data

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        inputFile= "recombinedDataSample.csv" 
        saveFile="heightDataSample.csv"
    elif(sample == "n"):
        inputFile= "recombinedData.csv" 
        saveFile="heightData.csv"

    folder = "../../pandafied_data/"

    print("load data")
    inputData = pd.read_csv(folder + inputFile)
    
    outputData = addHeightKwartetSearch(inputData)

    outputData.to_csv(folder+saveFile, index=False)