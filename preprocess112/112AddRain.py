import pandas as pd 
from tqdm import tqdm

def make_labels(data,label_on, saveFile):
    """
        Label the data set, empty examples in target column get label  0 all other 1.
        Parameters: 
            data: pandas dataframe to be labeled
            labeled_on: string, column name of pandas dataframe column to label on
        Output: pandas dataframe
        Source: Christiaan
    """
    labels = []
    print("make_labels:")
    for i in tqdm(data[label_on]):
        try:
            if np.isnan(i):
                num=0
            else:
                num=1
        except:
            num=1
        labels.append(num)
    data['labels'] = labels
    data.to_csv(saveFile, index=False)
    return data

def combineDataFrames(pd112, pdRain, saveFile):
    """

        Source: Christiaan
    """
    print("Preprocess tweets")

    #remove duplicates
    pd112 = pd112.drop_duplicates()
    
    pdRain = pdRain[pdRain['date'].notnull()]

    # Date into correct format
    pd112['date'] = pd.to_datetime(pd112['date'], format='%Y-%m-%d')
    pdRain['date'] = pd.to_datetime(pdRain['date'], format='%Y%m%d')

    print("Merge data")
    pd112Rain = pd.merge(pdRain, pd112, on=('radarX','radarY','date'), how='left')
    
    pd112Rain=pd112Rain[pd112Rain['rain'].notnull()]

    pd112Rain.to_csv(saveFile, index=False)
    return pd112Rain

if __name__ == '__main__':
    folder = '../../csv112/'
    pd112 = pd.read_csv(folder+'112XYSample.csv')
    rain = pd.read_csv(folder+'pandafied_h5_rain_2020.csv')
    output = combineDataFrames(pd112 = pd112, pdRain=rain, saveFile=folder+'112RainSample.csv')
    output.to_csv('../../csv112/test.csv', index=False )
    print(output)