import pandas as pd

def selectTweets(tweets):    
    tweets['date'] = tweets['date'].astype(str)
    tweets = tweets[~tweets['date'].str.contains('2019')]
    tweets = tweets[~tweets['date'].str.contains('2018')]
    tweets.to_csv(savefile, index=False)

    print(tweets)

def selectSampleTweets(tweets):
    tweets = pd.read_csv(tweetfile)
    
    tweets['date'] = tweets['date'].astype(str)
    tweets = tweets[tweets['date'].str.contains('201712')]

    tweets.to_csv(savefile, index=False)

    print(tweets)

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
        output=selectSampleTweets(tweets)
    elif sample == "n":
        savefile = 'twitter_2010-2017_XY.csv'
        output=selectTweets(tweets)

    output.to_csv(folder+savefile, index=False)

