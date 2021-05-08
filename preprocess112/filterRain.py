# 1. filter rain below threshold
import pandas as pd 

def filterRain(data, threshold, saveFile):
    '''

        Parameters:
            pos_data: pandas dataframe containing tweets
        Output: pandas dataframe
    '''

    print("Filter data")    
    data = data[data.rain> threshold]

    startDate = pd.Timestamp(2015,12,31)
    endDate = pd.Timestamp(2021,3,1)
    print("set proper date format")
    data.loc[:,'date'] = pd.to_datetime(data['date'], format='%Y%m%d')
    print("filter dates")
    data = data[(data['date']>startDate)&(data['date']<endDate)]
    data = data.reset_index(drop=True)
    data.to_csv(saveFile, index=False)
    return data

if __name__ == '__main__':  
    folder = "/data/s2155435/csv112/"

    print("load data")
    rain = pd.read_csv(folder + 'pandafied_h5_rain_2007-2020.csv')
    
    output = filterRain(rain, 10, folder+'rainFiltered.csv')

    print(output)