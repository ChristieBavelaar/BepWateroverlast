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
    endDate = pd.Timestamp(2020,3,1)
    data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
    ata = data[(data['date']>startDate)&(data['date']<endDate)]
    data = data.reset_index(drop=True)
    data.to_csv(saveFile, index=False)
    return data

if __name__ == '__main__':  
    folder = "../../csv112/"

    print("load data")
    rain = pd.read_csv(folder + 'pandafied_h5_rain_2020.csv')
    
    output = filterRain(rain, 10, folder+'rainFilteredSample.csv')

    print(output)