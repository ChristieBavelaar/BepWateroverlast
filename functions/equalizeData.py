def equalize_data(data):
    '''
        Since there are orders of magnitude more negative samples than positive samples, this method makes the amount of negative samples the same as the amount of positive samples, by random sampling from the negative samples.
        Also only allow tweets with rain > threshold
        Input: Panda's dataframe
        Output: Panda's dataframe
    '''

    print("Equalizing data")

    # divide in positive and negative samples
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]

    print("     nrPositive: " + str(len(pos_data)))
    print("     nrNegative: " + str(len(neg_data)))
    
    # add in an equal number of negative samples
    data=pos_data
    data = data.append(neg_data.sample(n=len(pos_data),replace=False))
    
    print("     Total: " + str(len(data)))
    return data.reset_index(drop=True)