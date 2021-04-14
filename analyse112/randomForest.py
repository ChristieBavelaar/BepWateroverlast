import pandas as pd 
import numpy as np 
import sys
import os
from numpy import savetxt
import matplotlib.pyplot as plt
#sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn import metrics

def randomForest(folder='/data/s2155435/csv112/', inputFile='finalData.csv'):
    #resultFolder = '/home/s2155435/bep1/analyse112/results/'
    resultFolder = './results/'
    resultFile = open (resultFolder+"resultRFAlice.txt", "w+")
    
    #load data
    rainTweets_eq = pd.read_csv(folder + inputFile)
    print("data loaded")

    print(rainTweets_eq.dtypes)

    rainTweets_eq= rainTweets_eq.drop(columns=['radarX', 'radarY', 'latitude', 'longitude', 'tiffile'])

    rainTweets_eq = rainTweets_eq.dropna()
    
    labels = np.array(rainTweets_eq['labels'])
    
    #set features and convert to numpy array
    #with height: features= rainTweets_eq.drop(columns=['radarX', 'radarY', 'date', 'text','tiffile', 'height','labels'])
    features= rainTweets_eq.drop(columns=['labels'])
    #features= rainTweets_eq.drop(columns=['labels', 'rain'])
    #features = rainTweets_eq[['rain']]
    
    # Saving feature names for later use
    feature_list = list(features.columns)
    
    features = np.array(features)
    
    #k-fold cross validation
    skf = StratifiedKFold(n_splits=10)
    mape = []
    treeNumber = 0
    accuracyResult = []
    precisionResult = []
    recallResult = []
    totalConfusion = [[0,0],[0,0]]
    for train_index, test_index in skf.split(features, labels):
        #print("Train: ", train_index, " Test: ", test_index)
        train_features, test_features = features[train_index], features[test_index]
        train_labels, test_labels = labels[train_index], labels[test_index]

        #print(test_features[0])
        #train and test the decision tree
        rf = RandomForestClassifier(n_estimators = 1000, random_state = 42)        
        rf.fit(train_features, train_labels)
        label_prediction = rf.predict(test_features)

        #output performance subtree
        #errors = abs(label_prediction - test_labels)
        #print('Mean Absolute Error:', round(np.mean(errors), 2))
        # Pull out one tree from the forest
        confusion = confusion_matrix(test_labels,label_prediction)
        totalConfusion[0][0] += confusion[0][0]
        totalConfusion[0][1] += confusion[0][1]
        totalConfusion[1][0] += confusion[1][0]
        totalConfusion[1][1] += confusion[1][1]

        accuracyResult.append(metrics.accuracy_score(test_labels, label_prediction))
        precisionResult.append(precision_score(test_labels, label_prediction))
        recallResult.append(recall_score(test_labels, label_prediction))

        resultFile.write("Fold "+str(treeNumber)+"\n")
        resultFile.write(str(confusion)+'\n')
        resultFile.write("Accuracy: "+str(metrics.accuracy_score(test_labels, label_prediction))+"\n")
        resultFile.write("Precision: "+str(precision_score(test_labels, label_prediction))+"\n")
        resultFile.write("Recall: "+str(recall_score(test_labels, label_prediction)) + "\n\n")
        
        tree = rf.estimators_[4]# Import tools needed for visualization
        from sklearn.tree import export_graphviz
        import pydot# Pull out one tree from the forest
        tree = rf.estimators_[5]# Export the image to a dot file
        outputFile = resultFolder+"tree"+str(treeNumber)+".dot"
        export_graphviz(tree, out_file = outputFile, feature_names = feature_list, rounded = True, precision = 1)# Use dot file to create a graph
        #(graph, ) = pydot.graph_from_dot_file('tree.dot')# Write graph to a png file
        #graph.write_png('tree.png')
        treeNumber+=1
        
    #output cross validation performance
    #all_accuracies = cross_val_score(estimator=rf, X=features, y=labels, cv=10)

    fig, ax = plt.subplots()
    data = [accuracyResult, precisionResult, recallResult]
    xlabels = ["Accuracy", "Precision", "Recall"]
    ax.boxplot(data)
    ax.set_xticklabels(xlabels)
    resultFile.write("\nAverage accuracy: "+str(np.average(accuracyResult))+"\n")
    resultFile.write("Average Precision: "+str(np.average(precisionResult))+"\n")
    resultFile.write("Average Recall: "+ str(np.average(recallResult))+"\n")
    resultFile.write("Total Confusion matrix: \n["+str(totalConfusion[0][0])+","+ str(totalConfusion[0][1])+"] \n"+"["+str(totalConfusion[1][0])+","+ str(totalConfusion[1][1])+"] \n")
    resultFile.close()
    #print(cross_val_score(estimator=rf, X=features, y=labels, cv=skf, scoring="accuracy"))
    plt.savefig(resultFolder+"boxplotMeasures.png")
    plt.show()
   
if __name__ == '__main__':
    
    if(sys.argv[1] == "y"):
        sampleFile="finalDataSample.csv"
        randomForest(folder="../../csv112/",inputFile=sampleFile)
    elif(sys.argv[1] == "n"):
        randomForest()
