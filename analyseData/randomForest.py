import pandas as pd 
import numpy as np 
import sys
import os

#sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn import metrics

def randomForest(folder='../../pandafied_data/', inputFile='finalData.csv'):
    resultFile = open ("./results/resultRF.txt", "w+")
    #load data
    rainTweets_eq = pd.read_csv(folder + sampleFile)
    print("data loaded")
    #print(rainTweets_eq)
    #rainTweets_eq = rainTweets_eq.dropna(subset=['0'])
    print(rainTweets_eq)
    #print(rainTweets_eq)
    #print(rainTweets_eq.columns)
    #set labels
    labels = np.array(rainTweets_eq['labels'])

    cols = [col for col in rainTweets_eq.columns if 'Unnamed' not in col]
    rainTweets_eq = rainTweets_eq[cols]


    #set features and convert to numpy array
    #with height: features= rainTweets_eq.drop(columns=['radarX', 'radarY', 'date', 'text','tiffile', 'height','labels'])
    features= rainTweets_eq.drop(columns=['radarX', 'radarY', 'date', 'text','labels', 'latlon', 'tiffile'])
    #features = rainTweets_eq[['rain']]
    
    # Saving feature names for later use
    feature_list = list(features.columns)
    
    features = np.array(features)

    #k-fold cross validation
    skf = StratifiedKFold(n_splits=10)
    mape = []
    for train_index, test_index in skf.split(features, labels):
        #print("Train: ", train_index, " Test: ", test_index)
        train_features, test_features = features[train_index], features[test_index]
        train_labels, test_labels = labels[train_index], labels[test_index]
        
        #train and test the decision tree
        rf = RandomForestClassifier(n_estimators = 1000, random_state = 42)        
        rf.fit(train_features, train_labels)
        label_prediction = rf.predict(test_features)

        #output performance subtree
        #errors = abs(label_prediction - test_labels)
        #print('Mean Absolute Error:', round(np.mean(errors), 2))
        # Pull out one tree from the forest
        resultFile.write("Accuracy:")
        resultFile.write(str(metrics.accuracy_score(test_labels, label_prediction))+'\n')
        resultFile.write(str(confusion_matrix(test_labels,label_prediction))+'\n\n')
        
        tree = rf.estimators_[4]# Import tools needed for visualization
        from sklearn.tree import export_graphviz
        import pydot# Pull out one tree from the forest
        tree = rf.estimators_[5]# Export the image to a dot file
        outputFile = "./results/tree"+str(test_index)+".dot"
        export_graphviz(tree, out_file = outputFile, feature_names = feature_list, rounded = True, precision = 1)# Use dot file to create a graph
        #(graph, ) = pydot.graph_from_dot_file('tree.dot')# Write graph to a png file
        #graph.write_png('tree.png')
        
    #output cross validation performance
    all_accuracies = cross_val_score(estimator=rf, X=features, y=labels, cv=9)

    resultFile.write(all_accuracies)
    resultFile.close()
    #print(cross_val_score(estimator=rf, X=features, y=labels, cv=skf, scoring="accuracy"))
   
if __name__ == '__main__':
    
    if(sys.argv[1] == "y"):
        sampleFile="finalDataSample.csv"
        randomForest(inputFile=sampleFile)
    elif(sys.argv[1] == "n"):
        randomForest()