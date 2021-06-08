import pandas as pd

from combineData import combineDataFrames
from labelData import make_labels
from seperateData import seperateData
folder = "/data/s2155435/pandafied_data/"
samplename=''
data = pd.read_csv(folder+"twitter_2010-2017_XY_tiff.csv")
rain = pd.read_csv(folder+"pandafied_h5_rain_2007-2020.csv")
print("Preprocess tweets")
#pick relevant columns from tweets_XY
data['date'] = data['date'].astype('object')
data = data.drop(columns=['time'])
#remove duplicates
data = data.drop_duplicates()

rain = rain[rain['date'].notnull()]
rain['date'] = rain['date'].astype('object')

rain = rain.reset_index(drop=True)

print("Merge data")
print(data)
print(rain)
data = pd.merge(rain, data, on=('radarX','radarY','date'), how='left')
data=data[data['rain'].notnull()]
data = data.reset_index(drop=True)

data = make_labels(data, 'text', folder+'labeledDataUnfiltered'+samplename+'.csv')
posData, negData = seperateData(data, folder+'posDataUnfiltered'+samplename+'.csv', folder+'negDataUnfiltered'+samplename+'.csv')