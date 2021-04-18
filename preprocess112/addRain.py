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

if __name__ == '__main__':
    folder = '../../csv112/'
    pd112 = pd.read_csv(folder+'112XYSample.csv')
    rain = pd.read_csv(folder+'rainFilteredSample.csv')
    output = combineDataFrames(pd112 = pd112, pdRain=rain, saveFile=folder+'112RainSample.csv')
    print(output)