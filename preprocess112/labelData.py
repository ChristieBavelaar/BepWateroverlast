# 2 label data and save seperately
import pandas as pd 
import numpy as np
from tqdm import tqdm

def make_labels(data,label_on, saveFilePos, saveFileNeg):
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

    print(data)
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]

    pos_data.to_csv(saveFilePos, index = False)
    neg_data.to_csv(saveFileNeg, index=False)
    return pos_data, neg_data

if __name__ == '__main__':
    folder = '../../csv112/'
    inputdata = pd.read_csv(folder+'112RainSample.csv')
    posOutput, negOutput = make_labels(data=inputdata, label_on='latitude', saveFilePos=folder+'112LabeledSample.csv', saveFileNeg=folder+'rainLabeledSample.csv')
    print(posOutput)
    print(negOutput)