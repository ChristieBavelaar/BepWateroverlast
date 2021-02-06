import pandas as pd

def selectTweets(tweetfile='../../pandafied_data/pandafied_twitter_2007-2020_XY.csv', savefile="../../pandafied_data/twitter_2010-2017_XY.csv"):
    tweets = pd.read_csv(tweetfile)
    
    tweets['date'] = tweets['date'].astype(str)
    tweets = tweets[~tweets['date'].str.contains('2019')]
    tweets = tweets[~tweets['date'].str.contains('2018')]
    tweets.to_csv(savefile, index=False)

    print(tweets)

def selectSampleTweets(tweetfile='../../pandafied_data/pandafied_twitter_2007-2020_XY.csv', savefile="../../pandafied_data/pandafied_twitter_2017_12.csv"):
    tweets = pd.read_csv(tweetfile)
    
    tweets['date'] = tweets['date'].astype(str)
    tweets = tweets[tweets['date'].str.contains('201712')]

    tweets.to_csv(savefile, index=False)

    print(tweets)

if __name__ == '__main__':
    sample = input("Sample? y/n \n")
    if sample == "y":
        selectSampleTweets()
    elif sample == "n":
        selectTweets()
