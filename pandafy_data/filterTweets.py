import pandas as pd 

def filter_tweets(data, threshold, saveFile):
    '''
        Filter out all positive examples to have a rain > threshold
        Parameters:
            pos_data: pandas dataframe containing tweets
        Output: pandas dataframe
    '''
    # divide in positive and negative samples
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]

    print("     nrPositive: " + str(len(pos_data)))
    print("     nrNegative: " + str(len(neg_data)))

    print("Filter data")    
    data = data[data.rain> threshold]

    data = data.reset_index(drop=True)
    data.to_csv(saveFile, index=False)
    return pos_data

if __name__ == '__main__':
    sample = input("Sample? y/n")
    if(sample == "y"):
        inputFile= "posDataSample.csv" 
        saveFile="filteredTweetsSample.csv"
    elif(sample == "n"):
        inputFile= "posData.csv" 
        saveFile="filteredTweets.csv"
    
    folder = "../../pandafied_data/"

    print("load data")
    tweets_XY = pd.read_csv(folder + inputFile)
    
    filterTweets = filter_tweets(tweets_XY, 0, folder+saveFile)
