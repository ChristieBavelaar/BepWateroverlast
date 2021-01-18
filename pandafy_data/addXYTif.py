import pandas as pd 
import numpy as np 

def load_pandafied(folder='../../pandafied_data/', radarFile = "pandafied_h5_radar.csv", tifFile="lat_lon_to_filename.csv"):
    print("load radar data")
    radar = pd.read_csv(folder + radarFile)
    print("load tif data")
    tif = pd.read_csv(folder + tifFile)
    return radar, tif

def combineDataFrames(folder='../../pandafied_data/', radarFile = "pandafied_h5_radar.csv", tifFile="lat_lon_to_filename.csv", saveFile="tifFilename_XY.csv"):
    #first load the data
    radar,tif = load_pandafied(folder=folder, radarFile=radarFile, tifFile=tifFile)

    #merge dataset
    radarTif = pd.merge(radar, tif, on=('latlon_sw', 'latlon_se', 'latlon_ne', 'latlon_nw'), how='inner')
    
    #print and save
    print(radarTif)
    radarTif.to_csv(folder+saveFile, index=False)
    return radarTif

if __name__ == '__main__':
    default = input("Default? y/n")
    if(default == "n"):
        radarFile=input("Enter file name of rader data:")
        tifFile=input("Enter file name of tif data:")
        saveFile=input("Enter name of save file:")
        combineDataFrames(radarFile=radarFile, tifFile=tifFile, saveFile=saveFile)
    elif(default == "y"):
        combineDataFrames()