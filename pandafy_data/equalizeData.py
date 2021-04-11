import pandas as pd 

def equalize_data(data, saveFile, extra=1):
    '''
        Since there are orders of magnitude more negative samples than positive samples, this function creates an equal amount of positive and negative samples, by random sampling from the negative samples.
        Parameters: 
            data: pandas data frame containing samples to turned into equal amount of positives and negatives.
        Output: Panda's dataframe
        Source: Christiaan
    '''

    print("Equalizing data")

    # divide in positive and negative samples
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]

    print("     nrPositive: " + str(len(pos_data)))
    print("     nrNegative: " + str(len(neg_data)))
    
    # add in an equal number of negative samples
    data=pos_data
    data = data.append(neg_data.sample(n=len(pos_data)*extra,replace=False))
    
    print("     Total: " + str(len(data)))
    data = data.reset_index(drop=True)
    data.to_csv(saveFile, index=False)
    return data

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        inputFile = "labeledDataSample.csv" 
        saveFile="equalizedDataSample.csv"
    elif(sample == "n"):
        inputFile = "labeledData.csv"
        saveFile="equalizedData.csv"
    
    folder = "../../pandafied_data/"

    print("Load data")
    rainTweets = pd.read_csv(folder + inputFile)

    rainTweets_eq = equalize_data(data=rainTweets, saveFile=folder+saveFile)