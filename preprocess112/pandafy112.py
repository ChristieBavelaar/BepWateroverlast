import pandas as pd 

def pandafy112(folder = '../../', alice=False):
     # Write to csv file
    #folder = '/data/s2155435/'
    pd112 = pd.read_json(folder+'parsed_w_precise_coords.json')
    pd112.to_csv(folder+'csv112/112Full.csv', index=False)
    
    # Select relevant columns
    pd112 = pd112[['date', 'latitude', 'longitude']]
    pd112['date'] = pd.to_datetime(pd112['date'], format='%Y-%m-%d')
    pd112['hour'] = pd112['date'].dt.hour
    pd112['date'] = pd112['date'].dt.date
    pd112['labels'] = [1] * len(pd112.index)
    pd112.to_csv(folder+'csv112/112Relevant.csv', index=False)
    
    if not alice:
        # Select sample
        startDate = pd.Timestamp(2017,12,1)
        endDate = pd.Timestamp(2018,1,1)
        pd112Sample = pd112[(pd112['date'] > startDate) & (pd112['date']<endDate)]
        pd112Sample.to_csv(folder+'csv112/112RelevantSample.csv', index=False, date_format='%Y-%m-%d')
        return pd112Sample
    return pd112

if __name__ == '__main__':
    pandafy112()
