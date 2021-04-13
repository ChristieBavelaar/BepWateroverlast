import pandas as pd 

def equalize(data, saveFile):
    print("Equalizing data")
    data = data.drop(columns=['date'])
    data = data.dropna()
    print(data)
    # divide in positive and negative samples
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]

    print("     nrPositive: " + str(len(pos_data)))
    print("     nrNegative: " + str(len(neg_data)))
    
    # add in an equal number of negative samples
    data=pos_data
    data = data.append(neg_data.sample(n=len(pos_data),replace=False))
    
    print("     Total: " + str(len(data)))
    data = data.reset_index(drop=True)
    data.to_csv(saveFile, index=False)
    return data

if __name__ == '__main__':
    folder = '../../csv112/'
    pdRandom = pd.read_csv(folder + 'randomHeightSample.csv')
    pdAdress = pd.read_csv(folder + 'adressHeightSample.csv')

    outputRandom = equalize(data=pdRandom, saveFile=folder+'randomEqualSample.csv')
    print(outputRandom)

    outputAdress = equalize(data=pdAdress, saveFile=folder+'adressEqualSample.csv')
    print(outputAdress)
