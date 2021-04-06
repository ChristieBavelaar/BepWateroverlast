import pandas as pd 

def dependent_sampling(pos_data, neg_data, saveFile1, saveFile2):
    # Create new data frame
    negEq = pd.DataFrame()

    # Add in the first sample
    # Choose a sample from a dataframe with negative examples having the same radarX and radarY
    temp = neg_data.loc[(neg_data['radarX'] == pos_data.iloc[0]['radarX']) & (neg_data['radarY'] == pos_data.iloc[0]['radarY']) ]
    negEq = negEq.append(temp.sample())

    for i in range(1,len(pos_data.index)):
        temp = neg_data.loc[(neg_data['radarX'] == pos_data.iloc[i]['radarX']) & (neg_data['radarY'] == pos_data.iloc[i]['radarY']) ]
        newRow = temp.sample()

        # When to positive examples in the same radar space occur it is possible to add in a duplicate. Check that the sample is not allready contained in negEq
        while not negEq.loc[(negEq['radarX'] == newRow.iloc[0]['radarX']) & (negEq['radarY'] == newRow.iloc[0]['radarY']) & (negEq['date'] == newRow.iloc[0]['date'])].empty:
            newRow = temp.sample()
        negEq = negEq.append(newRow)

    # Add the same coordinates to the negative example as the positive examples
    negEq = negEq.reset_index(drop=True)
    pos_data = pos_data.reset_index(drop=True)
    negEq['latlon'] = pos_data['latlon']
    negEq['tiffile'] = pos_data['tiffile']

    # Save to file
    pos_data.to_csv(saveFile1, index=False)
    negEq.to_csv(saveFile2, index=False)

    return pos_data, negEq

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        inputFile = "labeledDataSample.csv" 
        saveFile1="depSampPosSample.csv"
        saveFile2="depSampNegSample.csv"
    elif(sample == "n"):
        inputFile = "labeledData.csv"
        saveFile1="depSampPos.csv"
        saveFile2="depSampNeg.csv"
    
    folder = "../../pandafied_data/"

    print("Load data")
    rainTweets = pd.read_csv(folder + inputFile)

    print(dependent_sampling(data=rainTweets, saveFile1=folder+saveFile1, saveFile2=folder+saveFile2))