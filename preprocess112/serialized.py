# 6 create control
import sys 
import pandas as pd 

from pandafy112 import pandafy112
from pandafyTiff import pandafy_tiffs 
from pandafyRadar import pandafy_h5_make_radarXY
from KNMIRainSample import pandafy_h5_sample
from addXY import tweets_append_XY
from filterRain import filterRain
from addRain import combineDataFrames
from labelData import make_labels
from sampleNeg import randomSample, adressSample, dependent_sampling 
from addTiff import tweets_append_tif
from addHeight import addHeightKwartetSearch
from equalize import equalize

if __name__ == '__main__':
    print(sys.argv)
    if sys.argv[1] == 'y':
        alice = False
        samplename = 'Sample'
        folder = '../../'
    else:
        alice = True
        samplename = ''
        folder = '/data/s2155435/'

    threshold = int(sys.argv[2])
    samplemethod = int(sys.argv[3])
    start = int(sys.argv[4])

    if start == 1:
        pd112 = pandafy112(folder=folder, alice=alice)
        pdTif = pandafy_tiffs(data_folder=folder+'AHN2_5m/', save_name=folder+'csv112/lat_lon_to_filename.csv')
        pdRadar = pandafy_h5_make_radarXY(folder = folder + 'KNMI/RADNL_CLIM____MFBSNL25_01H_20170101T000000_20180101T000000_0002/RAD_NL25_RAC_MFBS_01H/2017/', save_name_radar=folder+'csv112/pandafied_h5_radar.csv')
        if alice:
            print("still to add full KNMI")
        else:
            pdRain = pandafy_h5_sample(save_name_radar=folder+'csv112/pandafied_h5_radar.csv',save_name_rain=folder+'csv112/pandafied_h5_rain_2020.csv',folder =folder+'KNMI/')
        start = 2

    if start == 2:
        pd112 = pd.read_csv(folder+'csv112/112Relevant'+samplename+'.csv')
        pdRadar = pd.read_csv(folder+'csv112/pandafied_h5_radar.csv')
        if alice:
            print("still to add full KNMI")
        else:
            pdRain = pd.read_csv(folder+'csv112/pandafied_h5_rain_2020.csv')

        data = tweets_append_XY(tweets=pd112, radar=pdRadar, saveFile=folder+'csv112/112XY'+samplename+'.csv')
        
        pdRain = filterRain(data=pdRain, threshold=threshold, saveFile=folder+'csv112/rainFiltered'+samplename+'.csv')

        start = 3

    if start == 3:
        pdRain = pd.read_csv(folder+'csv112/rainFiltered'+samplename+'.csv')
        data = pd.read_csv(folder+'csv112/112XY'+samplename+'.csv')

        data = combineDataFrames(pd112=data, pdRain=pdRain, saveFile=folder+'csv112/112Rain'+samplename+'.csv')

        start = 4

    if start == 4:
        data = pd.read_csv(folder+'csv112/112Rain'+samplename+'.csv')
        posData, negData = make_labels(data=data, label_on='latitude', saveFilePos=folder+'csv112/112Labeled'+samplename+'.csv', saveFileNeg=folder+'csv112/rainLabeled'+samplename+'.csv')

        start = 5

    if start == 5:
        posData = pd.read_csv(folder+'csv112/112Labeled'+samplename+'.csv')
        negData = pd.read_csv(folder+'csv112/rainLabeled'+samplename+'.csv')

        if samplemethod == 1:
            pdRadar = pd.read_csv(folder+'csv112/pandafied_h5_radar.csv')
            data = randomSample(data=negData, posData=posData, radar=pdRadar, extra=2, saveFile=folder+'csv112/sampled'+samplename+'.csv')
        elif samplemethod == 2:
            pdRadar = pd.read_csv(folder+'csv112/pandafied_h5_radar.csv')
            adresses = pd.read_csv(folder+'pandafied_data/verblijfplaatsen.csv')
            data = adressSample(adresses=adresses, posData=posData, negData=negData, radar=pdRadar, extra=2, saveFile=folder+'csv112/sampled'+samplename+'.csv', alice=alice)
        else:
            data = dependent_sampling(pos_data=posData, neg_data=negData, saveFile=folder+'csv112/sampled'+samplename+'.csv')

        start = 6

    if start == 6:
        data = pd.read_csv(folder+'csv112/sampled'+samplename+'.csv')
        pdTif = pd.read_csv(folder+'csv112/lat_lon_to_filename.csv')

        data = tweets_append_tif(tweets=data, tif=pdTif, saveFile=folder+'csv112/tif'+samplename+'.csv')

        start = 7
    
    if start == 7:
        data = pd.read_csv(folder+'csv112/tif'+samplename+'.csv')
        pdRadar = pd.read_csv(folder+'csv112/pandafied_h5_radar.csv')

        data = addHeightKwartetSearch(data=data, radar=pdRadar, saveFile=folder+'csv112/height'+samplename+'.csv', alice = alice)

        start = 8
    
    if start == 8:
        data = pd.read_csv(folder+'csv112/height'+samplename+'.csv')
        if samplemethod <=2:
            data = equalize(data=data, saveFile=folder+'csv112/finalData'+samplename+'.csv')
        else:
            data.to_csv(folder+'csv112/finalData'+samplename+'.csv')
        

    

    