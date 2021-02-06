from osgeo import osr,gdal
import sys
import math

import timeit
import numpy as np
from timeit import Timer

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

def getCoords(Xpixel, Ypixel, gt, transform):
    Xgeo = gt[0] + Xpixel*gt[1] + Ypixel*gt[2]
    Ygeo = gt[3] + Xpixel*gt[4] + Ypixel*gt[5]
    coordinates = transform.TransformPoint(Xgeo, Ygeo)
    return coordinates

#def fillKwartet(lX, rX, uY, lY):
    #spaceHorz = (rX-lX)/4
    #spaceVert = (uY-lY)/4

    #kwartet=[]
    #for i in [1, 3]:
        #for j in [1, 3]:
    #        kwartet.append([lX+i*spaceHorz, lY+j*spaceVert])
    #return kwartet

 #   mX = (lX+rX)/2
  #  mY = (lY+uY)/2
   # return [[lX, mX, uY, mY], [mX, rX, uY, mY], [lX, mX, mY, lY], [mX, rX, mY, lY]]

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

def kwartetSearch(folder='../../AHN2_5m/', filename='ahn2_5_38an2.tif', lat=52.016917, lon=4.713011):
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



def bruteForce(folder='../../AHN2_5m/', filename='ahn2_5_38an2.tif', lat=52.016917, lon=4.713011):
    #open file
    ds = gdal.Open(folder + filename)
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    transform = give_transform(ds,old_wkt=None) 
    
    #calculate find pixel with the smallest distance to given point
    minDist=math.inf
    minX=-1
    minY=-1
    for Xpixel in range(width):
        for Ypixel in range(height):
            #find coordinates of pixel
            Xgeo = gt[0] + Xpixel*gt[1] + Ypixel*gt[2]
            Ygeo = gt[3] + Xpixel*gt[4] + Ypixel*gt[5]
            coordinates = transform.TransformPoint(Xgeo, Ygeo)

            #find smallest value
            if math.dist([coordinates[0],coordinates[1]], [lat,lon])<minDist:
                minDist = math.dist([coordinates[0],coordinates[1]], [lat,lon])
                minX = Xpixel
                minY = Ypixel
    
    #print result
    Xgeo = gt[0] + minX*gt[1] + minY*gt[2]
    Ygeo = gt[3] + minX*gt[4] + minY*gt[5]
    coordinates = transform.TransformPoint(Xgeo, Ygeo)
    #print("looking for: ", lat, lon)
    #print("Closest to pixel: ("+ str(minX) +"," + str(minY) +") with latlon: "+str(coordinates) )
    
    #return result
    return minX,minY

if __name__ == '__main__':
    filename = 'ahn2_5_30fz1.tif'
    lat = 52.16944081767487
    lon = 4.456737798731557
    #kwartetSearch(filename=filename, lat=lat, lon=lon)
    print("kwartet",kwartetSearch())
    print("brute force",bruteForce())
    #print(fillKwartet(0, 20, 0, 10))
    
    expSize = 10


    t1 = Timer("kwartetSearch()", "from __main__ import kwartetSearch")
    st1 = t1.timeit(number=expSize)
    print("kwartet ",st1, "milliseconds")

    t2 = Timer("bruteForce()", "from __main__ import bruteForce")
    st2 = t2.timeit(number=expSize)
    print("Brute force ",st2, "milliseconds")