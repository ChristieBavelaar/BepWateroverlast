import pandas as pd
from osgeo import osr,gdal 
import sys
import os
import math

#import numpy as np 
import ast
import shapely
import shapely
from shapely.geometry import Polygon,Point
import random
from addTifTwitter import tweets_append_tif

def getCoords(Xpixel, Ypixel, gt, transform):
    Xgeo = gt[0] + Xpixel*gt[1] + Ypixel*gt[2]
    Ygeo = gt[3] + Xpixel*gt[4] + Ypixel*gt[5]
    coordinates = transform.TransformPoint(Xgeo, Ygeo)
    return coordinates

def give_transform(ds=None,old_to_new=True,old_wkt=None):
    #solution found at:
    #https://stackoverflow.com/questions/2922532/obtain-latitude-and-longitude-from-a-geotiff-file
    old_cs= osr.SpatialReference()
    #print(ds.GetProjectionRef())
    if not old_wkt is None:
        print("old_wkt is not None")
        old_cs .ImportFromWkt(old_wkt)
    elif not ds is None:
        old_cs.ImportFromWkt(ds.GetProjectionRef())
    else:
        print("missing projection information in pandafy_tiffs.give_transform()")
        exit()
    
    # create the new coordinate system
    wgs84_wkt = """
        GEOGCS["WGS 84",
        DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
        AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs .ImportFromWkt(wgs84_wkt)
    
    # create a transform object to convert between coordinate systems
    if old_to_new:
        return osr.CoordinateTransformation(old_cs,new_cs) 
    else:
        return osr.CoordinateTransformation(new_cs,old_cs) 

# sys.path.append(os.path.realpath('../functions/'))
# from findPixel import kwartetSearch
def fillKwartet(quarter):
    lX = quarter[0]
    rX = quarter[1]
    uY = quarter[2]
    lY = quarter[3]

    mX = (lX+rX)/2
    mY = (lY+uY)/2
    return [[lX, mX, uY, mY], [mX, rX, uY, mY], [lX, mX, mY, lY], [mX, rX, mY, lY]]

def findQuater(kwartet, lat, lon, gt, transform):
    bestDist = math.inf
    bestI = -1
    for i in range(4):
        mX = (kwartet[i][0] + kwartet[i][1]) / 2
        mY = (kwartet[i][2] + kwartet[i][3]) / 2
        
        coordinates = getCoords(mX, mY, gt, transform)
        currentDist = math.dist([coordinates[0],coordinates[1]], [lat,lon])
        if currentDist < bestDist:
            bestDist = currentDist
            bestI = i
    return kwartet[bestI]

def kwartetSearch(folder='/data/s2155435/AHN2_5m/', filename='ahn2_5_38an2.tif', lat=52.016917, lon=4.713011):
    #open file
    ds = gdal.Open(folder + filename)
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    transform = give_transform(ds,old_wkt=None) 
    #print("width ", width)
    #print("height ", height)
    rX = width
    uY = height
    lX = 1
    lY = 1
    quarter = [1,width, height, 1]
    

    while(quarter[1] - quarter[0] > 0.5 or quarter[2] - quarter[3] > 0.5):
        kwartet = fillKwartet(quarter)
        quarter = findQuater(kwartet, lat, lon, gt, transform)
        #print(quarter)
        #kwartet = fillKwartet(quarter)
    
    return int(quarter[0]+0.5), int(quarter[3]+0.5)

def addHeightKwartetSearch(data, saveFile):
    print("Add height")

    print("Load radar data")
    radar = pd.read_csv('/home/s2155435/pandafied_data/pandafied_h5_radar.csv')

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
            
            # open tiff file
            filepath = '/data/s2155435/AHN2_5m/' + data['tiffile'][i]
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
        except:
            #print(data['latlon'][i])
            dfArr = pd.DataFrame()
            print("An exception occured")
            
        
        
        # add dataframe to list
        listOfArr.append(dfArr)
    
    # initialise with first element of list
    dfOfArr = listOfArr[0]
    # add all other elements of the list
    for tw in range(1,len(listOfArr)):
        dfOfArr=dfOfArr.append(listOfArr[tw], ignore_index=True)
    
    # join the height data with existing data and save
    data=data.join(dfOfArr)

    data = data.dropna(axis='columns', how='all')
    data = data.dropna(thresh=10)
    data = data.reset_index(drop=True)
    data.to_csv(saveFile, index=False)

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
    
    outputData = addHeightKwartetSearch(inputData, folder+saveFile)