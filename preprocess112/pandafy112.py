import pandas as pd 

if __name__ == '__main__':
    # Write to csv file
    pd112 = pd.read_json('../../parsed_w_precise_coords.json')
    pd112.to_csv('../../csv112/112Full.csv', index=False)
    
    # Select relevant columns
    pd112 = pd112[['date', 'latitude', 'longitude']]

    # Add labels
    labels = [1] * len(pd112.index)
    pd112['labels'] = labels

    pd112.to_csv('../../csv112/112Relevant.csv', index=False)
    
    # Select sample
    startDate = pd.Timestamp(2020,1,1)
    endDate = pd.Timestamp(2020,12,31)
    pd112Sample = pd112[(pd112['date'] > startDate) & (pd112['date']<endDate)]
    pd112Sample.to_csv('../../csv112/112RelevantSample.csv', index=False)
