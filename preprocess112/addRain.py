import pandas as pd 
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
        day = pd.to_datetime(pdInput.iloc[i]['date'], format='%Y%m%d')
        dayData = rain[(rain['date']==day) & (rain['radarY']==pdInput.iloc[i]['radarY']) & (rain['radarX']==pdInput.iloc[i]['radarX'])]
        npDay = dayData.to_numpy()
        if nrHours > pdInput.iloc[i]['hour']:
            npDay = npDay[0,4:pdInput.iloc[i]['hour']+1]
            prevday = day - pd.Timedelta('1 days')
            prevDayData = rain[(rain['date']==prevday) & (rain['radarY']==pdInput.iloc[i]['radarY']) & (rain['radarX']==pdInput.iloc[i]['radarX'])]
            npPrevday = prevDayData.to_numpy()
            npPrevday = npPrevday[0, 4+(23 - (nrHours - pdInput.iloc[i]['hour'])):]

            totalPastRain = np.concatenate((npPrevday,npDay)).sum()
            pastRain.append(totalPastRain)
        else:
            npDay = npDay[0,4:nrHours+1].sum()
            pastRain.append(npDay)
    pdInput['rain'+str(nrHours)] = pastRain

def dayRain(pdInput,rain):
    dayRain = []
    for i in range(len(pdInput.index)):
        day = pd.to_datetime(pdInput.iloc[i]['date'], format='%Y%m%d')
        dayData = rain[(rain['date']==day) & (rain['radarY']==pdInput.iloc[i]['radarY']) & (rain['radarX']==pdInput.iloc[i]['radarX'])]
        npDay = dayData.to_numpy()
        dayRain.append(npDay[0,0])
    pdInput['rain'] = dayRain
    return pdInput

def rainAttributes(pdInput, rain, saveFile):
    print("Preprocess tweets")
    # pdInput['date'] = pdInput['date'].astype('object')
    pdInput['date'] = pd.to_datetime(pdInput['date'], format='%Y-%m-%d')
    print('Preprocess rain')
    rain['date']= pd.to_datetime(rain['date'], format='%Y%m%d')
    #rain['hour']=rain['hour'].astype(int)
    # rain['date'] = rain['dateh'].astype(str).str.slice(0,8).astype('object')
    # print('step1')
    # rain['hour'] = rain['dateh'].astype(str).str.slice(8,10).astype(int)
    pdInput = dayRain(pdInput,rain)
    for i in range(1,24):
        pdInput=addHourlyRain(pdInput,rain,i)
    

    try:
        pd112['hour'] = pd112['date'].dt.hour
    except:
        print("not pd112['hour'] = pd112['date'].dt.hour")
        
    try:
        pd112['date'] = pd112['date'].date
    except:
        print('not pd112[date].date')

    try:
        pd112['date'] = pd112['date'].dt.date
    except:
        print("not pd112['date'] = pd112['date'].dt.date")

    try:
        pd112['date'] = pd112['date'].date()
    except:
        print("not pd112['date'] = pd112['date'].date()")

    print(pdInput)
    pdInput.to_csv(saveFile, index=False)
    return pdInput
    
if __name__ == '__main__':
    folder = '/data/s2155435/csv112/'
    pd112 = pd.read_csv(folder+'depsamp2.csv')
    rain = pd.read_csv(folder+'rainFiltered.csv')
    output = combineDataFrames(pd112 = pd112, pdRain=rain, saveFile=folder+'112RainSample2.csv')
    print(output)