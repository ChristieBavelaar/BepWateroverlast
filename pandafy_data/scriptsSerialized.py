from pandafy_tiffs import pandafy_tiffs
from pandafy_twitter import pandafy_twitter
from pandafy_h5_make_radarXY import pandafy_h5_make_radarXY
from pandafy_twitter_add_XY import tweets_append_XY
from twitterSelect import selectTweets, selectSampleTweets
from KNMIRainSample import pandafy_h5
from addTifTwitter import tweets_append_tif
from combineData import combineDataFrames
from labelData import make_labels
from equalizeData import equalize_data
from seperateData import seperateData
from filterTweets import filter_tweets
from latlonTifNeg import addLatlonNegData
from addHeight import addHeightKwartetSearch
from recombinePosNeg import recombinePosNeg

if __name__ == '__main__':
    folder = "../../pandafied_data/"
    savefile = "labeledSample_eq.csv"

    print("From which step would like to start? (step 1-4 are not dependent) \n \
    1 give tiff files coordinates \n \
    2 pandafy twitter data \n \
    3 give radar XY coordinates \n \
    4 pandafy rain data \n \
    5 give tweets a radar XY \n \
    6 select tweets that apply to rain data \n \
    7 give each tweet a tif file \n \
    8 give each tweet a rain attribute \n \
    9 label the dataset \n \
    10 create equal number of positive and negative examples \n \
    11 seperate the dataset into positive and negative examples \n \
    12 filter positive examples below a rain threshold \n \
    13 give negative examples latlon and tif file \n \
    14 recombine positive and negative examples \n \
    15 add height attributes to examples\n \
    16 equalize the data again")

    startPoint = input("Give a starting number.")
    if(startPoint < 5):
        #1 give tiff files coordinates
        do1 = input("Do you want to perform step 1? y/n")
        if(do1 =="y" ):
            latlonTif = pandafy_tiffs()
        else:
            latlonTif = pd.read_csv(folder+"lat_lon_to_filename.csv")
        
        #2 pandafy twitter data
        do2 = input("Do you want to perform step 2? y/n")
        if(do2 =="y"):
            tweets = pandafy_twitter()
        else:
            tweets = pd.read_csv(folder+"pandafied_twitter_2007-2020.csv")

        #3 give radar XY coordinates
        do3 = input("Do you want to perform step 3? y/n")
        if(do3 =="y"):
            radar = pandafy_h5_make_radarXY()
        else:
            radar = pd.read_csv(folder+"pandafied_h5_radar.csv")

        sample = input("Do you want to do a sample run?")
        do4 = input("Do you want to perform step 4? y/n")
        #4 give tweets a radar XY
        if(do3 =="y"):
            tweetsXY = tweets_append_XY(tweets,radar)
        else:
            tweetsXY = pd.read_csv(folder+"pandafied_twitter_2007-2020_XY.csv")

    #5 select tweets that apply to rain data
    if(startPoint < 6):
        tweetsXY = selectSampleTweets(tweetsXY)
    else:
        tweet
    #6 pandafy twitter data
    rain = pandafy_h5()
    #7 give each tweet a tif file
    tweetsXYTif = tweets_append_tif(tweetsXY, latlonTif)
    #8 give each tweet a rain attribute
    combinedData = combineDataFrames(tweetsXYTif, rain)
    #9 label the dataset
    labeledData = make_labels(combineData, 'text')
    #10 create equal number of positive and negative examples
    equalizedData = equalize_data(labeledData)
    #11 seperate the dataset into positive and negative examples
    posData, negData = seperateData(equalizedData)
    #12 filter positive examples below a rain threshold
    filteredTweets = filter_tweets(posData)
    #13 give negative examples latlon and tif file
    latlonTifNeg = addLatlonNegData(negData)
    #14 recombine positive and negative examples
    recombinedData = recombinePosNeg(filteredTweets, latlonTifNeg)
    #15 add height attributes to examples
    heightData = addHeightKwartetSearch(recombinedData)
    #16 equalize the data again
    sampleData = equalize_data(heightData)

    sampleData.to_csv(folder+saveFile, index=False)
