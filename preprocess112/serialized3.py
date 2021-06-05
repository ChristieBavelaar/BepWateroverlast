# 6 create control
import sys 
import pandas as pd 

from pandafyRadar import pandafy_h5_make_radarXY
from pandafyTiff import pandafy_tiffs 

from pandafy112 import pandafy112
from KNMIRainSample import pandafy_h5_sample
from KNMIRainFull import pandafy_h5_full

from addXY import tweets_append_XY
from addHeight import addHeightKwartetSearch
from addTiff import tweets_append_tif

from filterRain import filterRain

from sampleNeg import dependent_sampling_2 

from addRain import dayRain
from addRain3 import rainAttributes2


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
        #folder='../../'
    threshold = int(sys.argv[2])
    start = float(sys.argv[3])

    if start == 1:
        pdTif = pandafy_tiffs(data_folder=folder+'AHN2_5m/', save_name=folder+'csv112/lat_lon_to_filename.csv')
        pdRadar = pandafy_h5_make_radarXY(folder = folder + 'KNMI/RADNL_CLIM____MFBSNL25_01H_20170101T000000_20180101T000000_0002/RAD_NL25_RAC_MFBS_01H/2017/', save_name_radar=folder+'csv112/pandafied_h5_radar.csv')
        start = 2

    if start == 2:
        pd112 = pandafy112(folder=folder, alice=alice)
        start = 3

    if start == 2.2:
        if alice:
            pdRain = pandafy_h5_full(save_name_radar=folder+'csv112/pandafied_h5_radar.csv',save_name_rain=folder+'csv112/pandafied_h5_rain_2016-2021.csv',folder =folder+'KNMI/')
        else:
            pdRain = pandafy_h5_sample(save_name_radar=folder+'csv112/pandafied_h5_radar.csv',save_name_rain=folder+'csv112/pandafied_h5_rain_2017_2.csv',folder =folder+'KNMI/')
        start = 3

    if start == 3:
        if alice:
            pdRain = pd.read_csv(folder+'csv112/pandafied_h5_rain_2010-2021.csv')
        else:
            pdRain = pd.read_csv(folder+'csv112/pandafied_h5_rain_2017_12.csv')

        pdRainFiltered = filterRain(data=pdRain, threshold=threshold, saveFile=folder+'csv112/rainFiltered'+samplename+'.csv', alice=alice)
        start=4
    
    if start == 4:
        pd112 = pd.read_csv(folder+'csv112/112Relevant'+samplename+'.csv')
        pdRadar = pd.read_csv(folder+'csv112/pandafied_h5_radar.csv')

        pd112 = tweets_append_XY(tweets=pd112, radar=pdRadar, saveFile=folder+'csv112/112XY'+samplename+'.csv')
        start =5 

    if start == 5:
        pdRainFiltered = pd.read_csv(folder+'csv112/rainFiltered'+samplename+'.csv')
        pd112 = pd.read_csv(folder+'csv112/112XY'+samplename+'.csv')

        pd112 = dayRain(pdInput=pd112, rain=pdRainFiltered, saveFile=folder+'csv112/112DayRain'+samplename+'.csv')
        start = 6

    if start == 6:
        pd112 = pd.read_csv(folder+'csv112/112DayRain'+samplename+'.csv')
        pdTif = pd.read_csv(folder+'csv112/lat_lon_to_filename.csv')

        pd112 = tweets_append_tif(tweets=pd112, tif=pdTif, saveFile=folder+'csv112/112Tif'+samplename+'.csv')
        start = 7

    if start == 7:
        pd112 = pd.read_csv(folder+'csv112/112Tif'+samplename+'.csv')
        pdRadar = pd.read_csv(folder+'csv112/pandafied_h5_radar.csv')

        pd112 = addHeightKwartetSearch(data=pd112, radar=pdRadar, saveFile=folder+'csv112/112Height'+samplename+'.csv', alice=alice)
        start =8
    
    if start == 8:
        pd112 = pd.read_csv(folder+'csv112/112Height'+samplename+'.csv')
        pdRainFiltered = pd.read_csv(folder+'csv112/rainFiltered'+samplename+'.csv')

        pdData = dependent_sampling_2(pos_data=pd112, rain=pdRainFiltered, saveFile=folder+'csv112/depSamp' + samplename+'.csv')
        start =9

    if start == 9:
        pdData = pd.read_csv(folder+'csv112/depSamp' + samplename+'.csv')
        if alice:
            pdRain = pd.read_csv(folder+'csv112/pandafied_h5_rain_2010-2021.csv')
        else:
            pdRain = pd.read_csv(folder+'csv112/pandafied_h5_rain_2017_12.csv')

        pdData = rainAttributes(pdInput=pdData, rain=pdRain, saveFile=folder+'csv112/hourlyAverageRain'+samplename+'.csv')

    
        

    

    