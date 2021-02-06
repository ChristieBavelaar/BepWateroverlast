def filter_tweets(data, threshold):
    '''
        filter all positive examples to have a rain > threshold
    '''

    print("Filter data")

    # divide in positive and negative samples
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]
    
    #filter tweets with too little rain
    pos_data = pos_data[pos_data.rain> threshold]
    
    # add negative samples
    data=pos_data
    data = data.append(neg_data)
    
    return data.reset_index(drop=True)