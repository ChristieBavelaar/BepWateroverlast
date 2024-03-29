import pandas as pd 
import numpy as np 
import sys
import os

#sklearn
from sklearn.tree import DecisionTreeClassifier 
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

#self-made functions
sys.path.append(os.path.realpath('../functions/'))
from equalizeData import equalize_data
from filterTweets import filter_tweets
sys.path.append(os.path.realpath('../pandafy_data/'))

def decisionTree(folder='../../pandafied_data/', inputFile='labeledSample.csv'):
    #load data
    rainTweets_eq = pd.read_csv(folder + sampleFile)
    print("data loaded")
    #filter out instances with no rain
    #rainTweets = filterTwitter(data=rainTweets, threshold=0)
   
    #create sampleset with equal number of positive and negative examples
    #rainTweets_eq = equalize_data(rainTweets)
    #rainTweets_eq.to_csv("../../pandafied_data/raintweets_eq.csv", index=False)

    #set labels
    labels = np.array(rainTweets_eq['labels'])
    
    #set features and convert to numpy array
    #with height: features= rainTweets_eq.drop(columns=['radarX', 'radarY', 'date', 'text','tiffile', 'height','labels'])
    features= rainTweets_eq.drop(columns=['radarX', 'radarY', 'date', 'text','labels', 'latlon','tiffile'])
    
    features = np.array(features)

    #k-fold cross validation
    skf = StratifiedKFold(n_splits=2)
    for train_index, test_index in skf.split(features, labels):
        #print("Train: ", train_index, " Test: ", test_index)
        train_features, test_features = features[train_index], features[test_index]
        train_labels, test_labels = labels[train_index], labels[test_index]
         #train and test the decision tree
        clf = DecisionTreeClassifier()
        clf.fit(train_features, train_labels)
        label_prediction = clf.predict(test_features)
        text_representation = tree.export_text(clf)

        #output performance subtree
        print(confusion_matrix(test_labels, label_prediction))
        print(classification_report(test_labels, label_prediction))
    
    #output cross validation performance
    print("Accuracy: ")
    print(cross_val_score(estimator=clf, X=features, y=labels, cv=skf, scoring="accuracy"))
   
if __name__ == '__main__':
    sample = input("Sample? y/n \n")
    if(sample == "y"):
        sampleFile="labeledSample_eq.csv"
        decisionTree(inputFile=sampleFile)
    elif(sample == "n"):
        decisionTree()
