import pandas as pd 
import numpy as np
from tqdm import tqdm

def combineDataFrames(pd112, pdRain, saveFile):
    """

        Source: Christiaan
    """
    print("Preprocess tweets")

    #remove duplicates
    pd112 = pd112.drop_duplicates()
    
    pdRain = pdRain[pdRain['date'].notnull()]

    # Normalize dates
    pd112['date'] = pd.to_datetime(pd112['date'], format='%Y-%m-%d').dt.date
    pdRain['date'] = pd.to_datetime(pdRain['date'], format='%Y-%m-%d').dt.date

    print(pd112)
    print(pdRain)
    print("Merge data")
    pd112Rain = pd.merge(pdRain, pd112, on=('radarX','radarY','date'), how='left')
    print(pd112Rain)
    #pd112Rain=pd112Rain[pd112Rain['rain'].notnull()]

    pd112Rain.to_csv(saveFile, index=False)
    return pd112Rain

def addHourlyRain(pdInput, rain, nrHours):
    pastRain = []
    for i in range(len(pdInput.index)):
        #day = pd.to_datetime(pdInput.iloc[i]['date'], format='%Y%m%d')
        day = pdInput.iloc[i]['date']
        dayData = rain[(rain['date']==day) & (rain['radarY']==pdInput.iloc[i]['radarY']) & (rain['radarX']==pdInput.iloc[i]['radarX'])]
        npDay = dayData.to_numpy()
        #print(npDay)
        if nrHours > pdInput.iloc[i]['hour']:
            npDay = npDay[0,4:pdInput.iloc[i]['hour']+1]
            prevday = day - pd.Timedelta('1 days')
            prevDayData = rain[(rain['date']==prevday) & (rain['radarY']==pdInput.iloc[i]['radarY']) & (rain['radarX']==pdInput.iloc[i]['radarX'])]
            
            npPrevday = prevDayData.to_numpy()
            npPrevday = npPrevday[0, 4+(24 - (nrHours - pdInput.iloc[i]['hour'])):]

            totalPastRain = np.concatenate((npPrevday,npDay)).sum()
            pastRain.append(totalPastRain)
        else:
            npDay = npDay[0,4:nrHours+1].sum()
            pastRain.append(npDay)

    pdInput['rain'+str(nrHours)] = pastRain

    print(nrHours,'/ 24')
    return pdInput

def dayRain(pdInput,rain, saveFile):
    print("Preprocess tweets") 
    pdInput['date'] = pd.to_datetime(pdInput['date'], format='%Y-%m-%d')

    print('Preprocess rain') 
    rain['date']= pd.to_datetime(rain['date'], format='%Y-%m-%d')

    dayRain = []
    for i in range(len(pdInput.index)):
        day = pdInput.iloc[i]['date']
        dayData = rain[(rain['date']==day) & (rain['radarY']==pdInput.iloc[i]['radarY']) & (rain['radarX']==pdInput.iloc[i]['radarX'])]
        try:
            npDay = dayData.to_numpy()
            dayRain.append(npDay[0,0])
        except:
            print('No rain for that alert')
            dayRain.append(None)
    pdInput['rain'] = dayRain

    print(pdInput)
    pdInput = pdInput.dropna()
    pdInput.to_csv(saveFile, index=False)
    return pdInput

def rainAttributes(pdInput, rain, saveFile):
    print("add daily rain")
    print("Preprocess tweets")
    # pdInput['date'] = pdInput['date'].astype('object')
    # rain['date'] = rain['date'].astype('object')
    pdInput['date'] = pd.to_datetime(pdInput['date'], format='%Y-%m-%d')
    pdInput['hour'] = pdInput['hour'].astype(int)

    print('Preprocess rain')
    rain['date']= pd.to_datetime(rain['date'], format='%Y%m%d')

    #rain['hour']=rain['hour'].astype(int)
    # rain['date'] = rain['dateh'].astype(str).str.slice(0,8).astype('object')
    # print('step1')
    # rain['hour'] = rain['dateh'].astype(str).str.slice(8,10).astype(int)
    # pdInput = dayRain(pdInput,rain)
    for i in range(1,25):
        print(i, "/ 24")
        pdInput=addHourlyRain(pdInput,rain,i)
    

    print(pdInput)
    pdInput.to_csv(saveFile, index=False)
    return pdInput
    
if __name__ == '__main__':
    folder = '../../csv112/'
    pd112 = pd.read_csv(folder+'112XYSample2020.csv')
    rain = pd.read_csv(folder+'rainFilteredSample.csv')
    output = dayRain(pdInput = pd112, rain=rain, saveFile=folder+'112RainSample2.csv')
    # output = rainAttributes(pd112, rain, folder+"112RainDepSamp.csv")

    # folder = '../../csv112/'
    # pd112 = pd.read_csv(folder+'112SampledSample.csv')
    # pd112_2 = pd.read_csv(folder+'112XYSample.csv')
    # rain = pd.read_csv(folder+'rainFilteredSample.csv')
    # rain_2 = pd.read_csv(folder+'pandafied_h5_rain_2017_12.csv')
    # #output = combineDataFrames(pd112 = pd112, pdRain=rain, saveFile=folder+'112RainSample2.csv')
    # output = rainAttributes(pd112, rain_2, folder+"112RainSumSample.csv")
    # # output = dayRain(pd112_2, rain, folder+'112DayRainSample.csv')

    print(output)