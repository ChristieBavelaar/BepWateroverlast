import pandas as pd 
from addRain import combineDataFrames
from labelData import make_labels

samplename = ''
folder = '/data/s2155435/'    
pdRain = pd.read_csv(folder+'csv112/pandafied_h5_rain_2020.csv')
data = pd.read_csv(folder+'csv112/112XY'+samplename+'.csv')

data = combineDataFrames(pd112=data, pdRain=pdRain, saveFile=folder+'csv112/112RainUnfiltered'+samplename+'.csv')

posData, negData = make_labels(data=data, label_on='latitude', saveFilePos=folder+'csv112/112Labeled'+samplename+'.csv', saveFileNeg=folder+'csv112/rainLabeledUnfiltered'+samplename+'.csv')