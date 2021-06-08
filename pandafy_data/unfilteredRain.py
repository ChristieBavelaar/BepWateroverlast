import pandas as pd

from combineData import combineDataFrames
from labelData import make_labels
from seperateData import seperateData
data = pd.read_csv(folder+"twitter_2010-2017_XY_tiff.csv")
rain = pd.read_csv(folder+"pandafied_h5_rain_2007-2020.csv")
folder = "/data/s2155435/pandafied_data/"
samplename=''
data = combineDataFrames(data, rain, folder+'combinedDataUnfiltered'+samplename+'.csv')
data = make_labels(data, 'text', folder+'labeledDataUnfiltered'+samplename+'.csv')
posData, negData = seperateData(data, folder+'posDataUnfiltered'+samplename+'.csv', folder+'negDataUnfiltered'+samplename+'.csv')