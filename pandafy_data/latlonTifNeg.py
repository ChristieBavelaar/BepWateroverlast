import pandas as pd 
import ast
import shapely
import shapely
from shapely.geometry import Polygon,Point
import random
from addTifTwitter import tweets_append_tif

def addLatlonNegData(neg_data, saveFile):
    """
        Negative samples in the data are assigned a random point within the KNMI rain area. Then a corresponding tif-File is found.
        Parameters:
            neg_data: pandas dataframe with negative examples
        Output: pandas dataframe
    """
    print("Load data")
    folder = '../../pandafied_data/'
    tif= pd.read_csv(folder+'lat_lon_to_filename.csv')
    radar = pd.read_csv(folder+'pandafied_h5_radar.csv')
    
    neg_data = pd.merge(neg_data, radar, on=('radarX','radarY'), how='left')

    print("Determine coordinates")
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
                break
    
    print("Find tif-file")
    neg_data = tweets_append_tif(neg_data, tif, saveFile)

    
    neg_data = neg_data.drop(columns=['latlon_center','latlon_ne',"latlon_nw", 'latlon_se', 'latlon_sw'])
    neg_data.to_csv(saveFile, index=False)
    return neg_data

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        inputFile= "negDataSample.csv" 
        saveFile="latlonTifNegSample.csv"
    elif(sample == "n"):
        inputFile= "negData.csv" 
        saveFile="latlonTifNeg.csv"

    folder = "../../pandafied_data/"

    print("load data")
    neg_data = pd.read_csv(folder + inputFile)

    outputData = addLatlonNegData(neg_data, folder+saveFile)
