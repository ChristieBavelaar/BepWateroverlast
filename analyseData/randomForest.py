import pandas as pd 
import numpy as np 
import sys
import os

#sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

def randomForest(folder='../../pandafied_data/', inputFile='labeledSample.csv'):
    #load data
    rainTweets_eq = pd.read_csv(folder + sampleFile)
    print("data loaded")

    #set labels
    labels = np.array(rainTweets_eq['labels'])
    
    #set features and convert to numpy array
    #with height: features= rainTweets_eq.drop(columns=['radarX', 'radarY', 'date', 'text','tiffile', 'height','labels'])
    features= rainTweets_eq.drop(columns=['radarX', 'radarY', 'date', 'text','labels', 'latlon', 'tiffile'])
    
    features = np.array(features)

    #k-fold cross validation
    skf = StratifiedKFold(n_splits=2)
    for train_index, test_index in skf.split(features, labels):
        #print("Train: ", train_index, " Test: ", test_index)
        train_features, test_features = features[train_index], features[test_index]
        train_labels, test_labels = labels[train_index], labels[test_index]
        
        #train and test the decision tree
        rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)        
        rf.fit(train_features, train_labels)
        label_prediction = rf.predict(test_features)

        #output performance subtree
        errors = abs(label_prediction - test_labels)
        print('Mean Absolute Error:', round(np.mean(errors), 2))
    
    #output cross validation performance
    #print("Accuracy: ")
    #print(cross_val_score(estimator=rf, X=features, y=labels, cv=skf, scoring="accuracy"))
   
if __name__ == '__main__':
    sample = input("Sample? y/n \n")
    if(sample == "y"):
        sampleFile="labeledSample_eq.csv"
        randomForest(inputFile=sampleFile)
    elif(sample == "n"):
        randomForest()