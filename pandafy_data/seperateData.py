import pandas as pd 

def seperateData(data, saveFilePos, saveFileNeg):
    """
        Seperate a labeled dataset into positive and negative examples.
        Parameters:
            data: pandas dataframe
        Output:
            pandas data frame positive examples
            pandas data frame negative examples
    """
    data['labels'] = data['labels'].astype(int)
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels != 1]

    pos_data.to_csv(saveFilePos, index = False)
    neg_data.to_csv(saveFileNeg, index=False)
    return pos_data, neg_data

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        inputFile = "equalizedDataSample.csv" 
        saveFilePos="posDataSample.csv"
        saveFileNeg="negDataSample.csv"
    elif(sample == "n"):
        inputFile = "equalizedData.csv"
        saveFilePos="posData.csv"
        saveFileNeg="negData.csv"
    
    folder = "../../pandafied_data/"

    print("Load data")
    rainTweets_eq = pd.read_csv(folder + inputFile)

    posData, negData = seperateData(rainTweets_eq, folder+saveFilePos, folder+saveFileNeg) 