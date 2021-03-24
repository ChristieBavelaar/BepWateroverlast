import pandas as pd 
import numpy as np 
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



if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        inputFile = "combinedDataSample.csv" 
        saveFile="labeledDataSample.csv"
    elif(sample == "n"):
        inputFile = "combinedData.csv"
        saveFile="labeledData.csv"
    
    folder = "../../pandafied_data/"

    print("Load data")
    rainTweets = pd.read_csv(folder + inputFile)

    rainTweets = make_labels(rainTweets,'text', folder+saveFile)