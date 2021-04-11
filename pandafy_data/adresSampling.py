# select randomly as much adresses as positive examples
# Give adresses radar X and radarY
# Select random date from that radarXradarY

import pandas as pd 
import ast

from addTifTwitter import tweets_append_tif
from pandafy_twitter_add_XY import tweets_append_XY
# https://thomasv.nl/2014/03/rd-naar-gps/ rijkscoordinaten

import math
class Converter:
    RDOriginX = 155E3
    RDOriginY = 463E3
    GpsOriginLat = 52.1551744
    GpsOriginLon = 5.38720621
    def __init__(self):
        self.lat = []
        self.lon = []
        for i in range(0,11):
            self.lat.insert(i, [])
            self.lon.insert(i, [])
            self.lon.insert(i+1,[])

        ## Latitude calculation
        self.lat[0] = [0,1,3235.65389]
        self.lat[1] = [2,0,-32.58297]
        self.lat[2] = [0,2,-0.2475]
        self.lat[3] = [2,1,-0.84978]
        self.lat[4] = [0,3,-0.0665]
        self.lat[5] = [2,2,-0.01709]
        self.lat[6] = [1,0,-0.00738]
        self.lat[7] = [4,0,0.0053]
        self.lat[8] = [2,3,-3.9E-4]
        self.lat[9] = [4,1,3.3E-4]
        self.lat[10] = [1,1,-1.2E-4]
        
        ## Longitude calculation
        self.lon[0] = [1,0,5260.52916]
        self.lon[1] = [1,1,105.94684]
        self.lon[2] = [1,2,2.45656]
        self.lon[3] = [3,0,-0.81885]
        self.lon[4] = [1,3,0.05594]
        self.lon[5] = [3,1,-0.05607]
        self.lon[6] = [0,1,0.01199]
        self.lon[7] = [3,2,-0.00256]
        self.lon[8] = [1,4,0.00128]
        self.lon[9] = [0,0,2.2E-4]
        self.lon[10] = [2,0,-2.2E-4]
        self.lon[11] = [5,0,2.6E-4]

    def toLat(self,rdX,rdY):
        a = 0
        dX = 1E-5 * (rdX - self.RDOriginX)
        dY = 1E-5 * (rdY - self.RDOriginY)

        for i in range(0,11):
            a = a + ( self.lat[i][2] * math.pow(dX, self.lat[i][0]) * math.pow(dY, self.lat[i][1]) )

        return round(self.GpsOriginLat + ( a / 3600 ), 9)

    def toLon(self,rdX,rdY):
        a = 0
        dX = 1E-5 * (rdX - self.RDOriginX)
        dY = 1E-5 * (rdY - self.RDOriginY)
        
        for i in range(0,12):
            a = a + ( self.lon[i][2] * math.pow(dX,self.lon[i][0]) * math.pow(dY, self.lon[i][1]) )

        return round(self.GpsOriginLon + ( a / 3600 ), 9)

def adress_sampling(data, adresses, tif, radar, saveFile, alice):
    '''
        
    '''
    if alice:
        folder = '/data/s2155435/'
    else:
        folder = '../../'

     # divide in positive and negative samples
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]

    print("     nrPositive: " + str(len(pos_data)))
    print("     nrNegative: " + str(len(neg_data)))
    print("Adress Sampling")

    # add in an equal number of negative samples
    negativeSamples = adresses.sample(n=len(pos_data)*2,replace=False)

    # Convert rijksdriehoek coordinates to regular coordinates
    latlon = []
    converter = Converter()
    for i in range(len(negativeSamples['pos'])):
        # Split on space and save in list
        coords = str(negativeSamples.iloc[i]['pos']).split()

        # Convert into regular coordinates and save to string format used with tweets
        strLatlon = '('+str(converter.toLat(float(coords[0]),float(coords[1])))+', '+str(converter.toLon(float(coords[0]),float(coords[1])))+')'

        latlon.append(strLatlon)
    negativeSamples['latlon'] = latlon

    # Drop unnecessary columns
    negativeSamples = negativeSamples.drop(columns=['pos','ind','einddatum','huisnummer_id', 'id'])

    # Reset index
    negativeSamples = negativeSamples.reset_index(drop=True)

    # Add radar XY
    negativeSamples = tweets_append_XY(negativeSamples,radar,folder+"pandafied_data/radarNeg.csv")

    # Add tiffile
    negativeSamples = tweets_append_tif(negativeSamples,tif, folder+"pandafied_data/tifNeg.csv")

    # Add rain property
    rain = []
    for i in negativeSamples.index:
        temp = neg_data.loc[(neg_data['radarX'] == negativeSamples.iloc[i]['radarX']) & (neg_data['radarY'] == negativeSamples.iloc[i]['radarY']) ]
        try:
            rain.append(float(temp.sample(random_state=42)['rain'].values))
        except:
            print("no instance of rain found")
            rain.append(None)
    negativeSamples['rain'] = rain
    
    # Add labels
    labels = [0] * len(negativeSamples.index)
    negativeSamples['labels'] = labels

    # latlon = negativeSamples['latlon'].values.tolist()[0]
    # latlon_point = ast.literal_eval(str(latlon))
    data = pd.concat([pos_data, negativeSamples], ignore_index=True)

    print("     Total: " + str(len(data)))
    data = data.reset_index(drop=True)

    data.to_csv(saveFile, index=False)
    return data


if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        inputFile1 = "labeledDataSample.csv" 
        saveFile="equalizedDataSampleAdress.csv"
    elif(sample == "n"):
        inputFile = "labeledData.csv"
        saveFile="equalizedData.csv"
    
    folder = "../../pandafied_data/"
    inputFile2 = 'verblijfplaatsen.csv'

    print("Load data")
    radar = pd.read_csv(folder+'pandafied_h5_radar.csv')
    tif= pd.read_csv(folder+'lat_lon_to_filename.csv')
    tweets = pd.read_csv(folder + inputFile1)
    adresses = pd.read_csv(folder+inputFile2)

    rainTweets_eq = adress_sampling(data=tweets, tif=tif, radar=radar, adresses=adresses, saveFile=folder+saveFile)