import pandas as pd 

def pandafy112(folder = '../../', alice=False):
     # Write to csv file
    pd112 = pd.read_json(folder+'parsed_w_precise_coords.json')
    pd112.to_csv(folder+'csv112/112Full.csv', index=False)
    
    # Select relevant columns
    pd112 = pd112[['date', 'latitude', 'longitude']]
    pd112.to_csv(folder+'csv112/112Relevant.csv', index=False)
    
    if not alice:
        # Select sample
        startDate = pd.Timestamp(2020,1,1)
        endDate = pd.Timestamp(2020,12,31)
        pd112Sample = pd112[(pd112['date'] > startDate) & (pd112['date']<endDate)]
        pd112Sample.to_csv(folder+'csv112/112RelevantSample.csv', index=False, date_format='%Y-%m-%d')
        return pd112Sample
    return pd112

if __name__ == '__main__':
    pandafy112()
