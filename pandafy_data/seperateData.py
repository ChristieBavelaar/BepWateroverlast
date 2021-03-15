import pandas as pd 

def seperateData(data):
    """
        Seperate a labeled dataset into positive and negative examples.
        Parameters:
            data: pandas dataframe
        Output:
            pandas data frame positive examples
            pandas data frame negative examples
    """
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]

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

    posData, negData = seperateData(rainTweets_eq) 

    print("Save to files")
    posData.to_csv(folder+saveFilePos, index=False)
    negData.to_csv(folder+saveFileNeg, index=False)