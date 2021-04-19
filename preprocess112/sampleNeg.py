# 3 Select sample of neg data, give latlon and add to pos data
import pandas as pd 
import ast
import shapely
import shapely
from shapely.geometry import Polygon,Point
import random

from addXY import tweets_append_XY
from latlonConverter import Converter

def randomSample(data, posData, radar, extra, saveFile):
    data = data.sample(n=len(posData)*extra,replace=False)

    data = pd.merge(data, radar, on=('radarX','radarY'), how='left')

    print("Determine coordinates")
    for i in range(len(data['latlon_sw'])):
        sw = ast.literal_eval(str(data['latlon_sw'][i]))
        se = ast.literal_eval(str(data['latlon_se'][i]))
        ne = ast.literal_eval(str(data['latlon_ne'][i]))
        nw = ast.literal_eval(str(data['latlon_nw'][i]))

        polygon = Polygon(((sw[1], sw[0]), (se[1], se[0]), (ne[1], ne[0]), (nw[1], nw[0]), (sw[1], sw[0])))
        min_x, min_y, max_x, max_y = polygon.bounds
        
        while True:
            randomPoint = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
            if(polygon.contains(randomPoint)):
                data['latitude'][i] = randomPoint.y
                data['longitude'][i] = randomPoint.x
                break
    data=data.drop(columns=['latlon_sw','latlon_se','latlon_ne','latlon_nw','latlon_center'])
    data = pd.concat([data,posData], ignore_index=True)
    data.to_csv(saveFile, index=False)
    return data

def adressSample(adresses, posData, negData, radar, extra, saveFile, alice=False):
    if alice:
        folder = '/data/s2155435/csv112/'
    else:
        folder='../../csv112/'
    # add in an equal number of negative samples
    negativeSamples = adresses.sample(n=len(posData)*2,replace=False)
    
    # Convert rijksdriehoek coordinates to regular coordinates
    lat = []
    lon = []
    converter = Converter()
    for i in range(len(negativeSamples['pos'])):
        # Split on space and save in list
        coords = str(negativeSamples.iloc[i]['pos']).split()

        # Convert into regular coordinates and save to string format used with tweets
        lat.append(converter.toLat(float(coords[0]),float(coords[1])))
        lon.append(converter.toLon(float(coords[0]),float(coords[1])))

    negativeSamples['latitude'] = lat
    negativeSamples['longitude'] = lon

    # Drop unnecessary columns
    negativeSamples = negativeSamples.drop(columns=['pos','ind','einddatum','huisnummer_id', 'id'])

    # Reset index
    negativeSamples = negativeSamples.reset_index(drop=True)

    # Add radar XY
    negativeSamples = tweets_append_XY(negativeSamples,radar,folder+"radarNeg.csv")

    # Add rain property
    rain = []
    for i in negativeSamples.index:
        temp = negData.loc[(negData['radarX'] == negativeSamples.iloc[i]['radarX']) & (negData['radarY'] == negativeSamples.iloc[i]['radarY']) ]
        try:
            rain.append(float(temp.sample(random_state=42)['rain'].values))
        except:
            print("no instance of rain found")
            rain.append(None)
    negativeSamples['rain'] = rain
    
    # Add labels
    labels = [0] * len(negativeSamples.index)
    negativeSamples['labels'] = labels

    data = pd.concat([posData, negativeSamples], ignore_index=True)
    data.to_csv(saveFile, index=False)

    return data

def dependent_sampling(pos_data, neg_data, saveFile):
    # Create new data frame
    negEq = pd.DataFrame()

    # Add in the first sample
    # Choose a sample from a dataframe with negative examples having the same radarX and radarY
    temp = neg_data.loc[(neg_data['radarX'] == pos_data.iloc[0]['radarX']) & (neg_data['radarY'] == pos_data.iloc[0]['radarY']) ]
    negEq = negEq.append(temp.sample())

    for i in range(1,len(pos_data.index)):
        temp = neg_data.loc[(neg_data['radarX'] == pos_data.iloc[i]['radarX']) & (neg_data['radarY'] == pos_data.iloc[i]['radarY']) ]
        newRow = temp.sample()

        # When to positive examples in the same radar space occur it is possible to add in a duplicate. Check that the sample is not allready contained in negEq
        while not negEq.loc[(negEq['radarX'] == newRow.iloc[0]['radarX']) & (negEq['radarY'] == newRow.iloc[0]['radarY']) & (negEq['date'] == newRow.iloc[0]['date'])].empty:
            newRow = temp.sample()
        negEq = negEq.append(newRow)

    # Add the same coordinates to the negative example as the positive examples
    negEq = negEq.reset_index(drop=True)
    pos_data = pos_data.reset_index(drop=True)
    negEq['latitude'] = pos_data['latitude']
    negEq['longitude'] = pos_data['longitude']

    # Save to file
    data = pd.concat([pos_data, negEq], ignore_index=True)
    data.to_csv(saveFile, index=False)

    return data

if __name__ == '__main__':
    folder = '../../csv112/'
    radar = pd.read_csv(folder+'pandafied_h5_radar.csv')
    neg_data = pd.read_csv(folder+'rainLabeledSample.csv')
    pos_data = pd.read_csv(folder+'112LabeledSample.csv')
    adresses = pd.read_csv('../../pandafied_data/verblijfplaatsen.csv')
    # output = randomSample(data=neg_data, posData=pos_data, radar=radar, extra=2, saveFile=folder+'randomSampledSample.csv')
    # print(output)

    # output = adressSample(adresses=adresses, posData=pos_data, negData=neg_data, radar=radar, extra=2, saveFile=folder+'adressSampledSample.csv')
    # print(output)

    output = dependent_sampling(pos_data, neg_data, saveFile=folder+"depsamp.csv")
    print(output)