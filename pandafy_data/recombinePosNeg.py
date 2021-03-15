import pandas as pd 

def recombinePosNeg(pos_data, neg_data):
    """
        Recombine the filtered tweets and negative examples with coordinates.
        Parameters: 
            pos_data: pandas dataframe containing tweets
            neg_data: pandas dataframe containing negative examples
        Output: pandas dataframe
    """
    print("Combine positive and negative data")
    data = pos_data.append(neg_data, ignore_index = True)
    return data

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        negFile= "latlonTifNegSample.csv" 
        posFile = "filteredTweetsSample.csv"
        saveFile="recombinedDataSample.csv"
    elif(sample == "n"):
        negFile= "latlonTifNeg.csv" 
        posFile = "filteredTweets.csv"
        saveFile="recombinedData.csv"

    folder = "../../pandafied_data/"

    print("load data")
    pos_data = pd.read_csv(folder + posFile)
    neg_data = pd.read_csv(folder + negFile)
    
    outputData = recombinePosNeg(pos_data,neg_data)

    outputData.to_csv(folder+saveFile, index=False)