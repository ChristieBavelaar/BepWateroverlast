import pandas as pd 

def filter_tweets(pos_data, threshold, saveFile):
    '''
        Filter out all positive examples to have a rain > threshold
        Parameters:
            pos_data: pandas dataframe containing tweets
        Output: pandas dataframe
    '''

    print("Filter data")    
    pos_data = pos_data[pos_data.rain> threshold]

    pos_data = pos_data.reset_index(drop=True)
    pos_data.to_csv(saveFile, index=False)
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
