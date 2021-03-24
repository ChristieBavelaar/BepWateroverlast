import pandas as pd

def selectTweets(tweets, savefile):    
    tweets['date'] = tweets['date'].astype(str)
    tweets = tweets[~tweets['date'].str.contains('2019')]
    tweets = tweets[~tweets['date'].str.contains('2018')]
    
    tweets = tweets[tweets['radarX'].notnull()]
    tweets = tweets.reset_index(drop=True)

    tweets.to_csv(savefile, index=False)
    return tweets

def selectSampleTweets(tweets, savefile):
    tweets['date'] = tweets['date'].astype(str)
    tweets = tweets[tweets['date'].str.contains('201712')]
    tweets = tweets[tweets['radarX'].notnull()]
    tweets = tweets.reset_index(drop=True)
    
    tweets.to_csv(savefile, index=False)
    return tweets

if __name__ == '__main__':
    """ 
        Make the Twitter cover the same time span as the rain data. 
            Full data: leave out tweets from 2018 and 2019 as there is no KNMI data from this time.
            Sample: select all tweets from december 2017
    """
    folder = "../../pandafied_data/"
    tweets = pd.read_csv(folder+"pandafied_twitter_2007-2020_XY.csv")
    
    sample = input("Sample? y/n \n")
    if sample == "y":
        savefile = "pandafied_twitter_2017_12.csv"
        output=selectSampleTweets(tweets, folder+savefile)
    elif sample == "n":
        savefile = 'twitter_2010-2017_XY.csv'
        output=selectTweets(tweets, folder+savefile)


