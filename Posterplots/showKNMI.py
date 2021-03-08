import h5py
from osgeo import gdal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def showimage(filename):
    filepath = filename
    print(filepath)
    dataset = gdal.Open(filepath, gdal.GA_ReadOnly) # Note GetRasterBand() takes band no. starting from 1 not 0
    #band_ds = gdal.Open(dataset.GetSubDatasets()[0][0], gdal.GA_ReadOnly)
    band = dataset.GetRasterBand(1)
    arr = band.ReadAsArray()
    print('dataset')
    print(dataset)
    print('band')
    print(band)
    print('arr')
    print(arr)
    print('length: '+ str(len(arr)))
    plt.imshow(arr)
    plt.show()

def h5pyImage(filepath):
    h5 = h5py.File(filepath,'r')
    img = np.array(list(h5['image1/image_data']))
    img = img.flatten().tolist()
    plt.plot(img)
    plt.show()

def dataframeplot(filepath):
    rain = pd.read_csv(filepath)
    print(rain)
    rain=rain[rain['radarX'] == 429.0]
    rain=rain[rain['radarY'] == 420.0]
    # rain.filter(radar245.0,528.0)
    # print("dropped")
    # rain=rain.groupby('date').sum()
    print(rain)
    rain.plot(x='date', y='rain')
    plt.show()

if __name__ == '__main__':
    #showimage('../../KNMI/RADNL_CLIM____MFBSNL25_01H_20170101T000000_20180101T000000_0002/RAD_NL25_RAC_MFBS_01H/2017/12/RAD_NL25_RAC_MFBS_01H_201712132000_NL.h5')
    #h5pyImage('../../KNMI/RADNL_CLIM____MFBSNL25_01H_20170101T000000_20180101T000000_0002/RAD_NL25_RAC_MFBS_01H/2017/12/RAD_NL25_RAC_MFBS_01H_201712010100_NL.h5')
    dataframeplot("../../pandafied_data/pandafied_h5_rain_2017_12.csv")