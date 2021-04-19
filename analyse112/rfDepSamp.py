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
    resultFolder = '/home/s2155435/bep1/experiments/scripts/'
    #resultFolder = './results/'
    resultFile = open (resultFolder+"resultRFAlice.txt", "w+")
    
    #load data
    data = pd.read_csv(folder+inputFile)

    # Delete unneccesary columns
    data= data.drop(columns=['radarX', 'radarY', 'date','latitude', 'longitude', 'tiffile'])
    data = data.dropna()

    # Seperate data
    print(data)
    pos_data = data[data.labels == 1]
    neg_data = data[data.labels == 0]
    neg_data = neg_data.reset_index(drop=True)
    pos_data = pos_data.reset_index(drop=True)

    print("data loaded")    

    labelsPos = np.array(pos_data['labels'])
    labelsNeg = np.array(neg_data['labels'])

    # Set features and convert to numpy array
    featuresPos= pos_data.drop(columns=['labels'])
    featuresNeg= neg_data.drop(columns=['labels'])
    #features= rainTweets_eq.drop(columns=['labels', 'rain'])
    #features = rainTweets_eq[['rain']]
    
    # Saving feature names for later use
    feature_list = list(featuresPos.columns)
    
    print(featuresPos)
    print(featuresNeg)

    featuresPos = np.array(featuresPos)
    featuresNeg = np.array(featuresNeg)

    # k-fold cross validation
    skf = StratifiedKFold(n_splits=10)
    mape = []
    treeNumber = 0
    accuracyResult = []
    precisionResult = []
    recallResult = []
    totalConfusion = [[0,0],[0,0]]
    for train_index, test_index in skf.split(featuresPos, labelsPos):
        # Create training and test features and labels
        train_features_pos, test_features_pos = featuresPos[train_index], featuresPos[test_index]
        train_labels_pos, test_labels_pos = labelsPos[train_index], labelsPos[test_index]

        train_features_neg, test_features_neg = featuresNeg[train_index], featuresNeg[test_index]
        train_labels_neg, test_labels_neg = labelsNeg[train_index], labelsNeg[test_index]

        train_features = np.concatenate((train_features_pos, train_features_neg))
        test_features = np.concatenate((test_features_pos, test_features_neg))
        
        train_labels = np.concatenate((train_labels_pos, train_labels_neg))
        test_labels = np.concatenate((test_labels_pos, test_labels_neg))

        #train and test the decision tree
        rf = RandomForestClassifier(n_estimators = 1000, random_state = 42)        
        rf.fit(train_features, train_labels)
        label_prediction = rf.predict(test_features)

        # Save performance
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
        export_graphviz(tree, out_file = outputFile, feature_names = feature_list, rounded = True, precision = 1)# 
        treeNumber+=1

    fig, ax = plt.subplots()
    data = [accuracyResult, precisionResult, recallResult]
    xlabels = ["Accuracy", "Precision", "Recall"]
    ax.boxplot(data)
    ax.set_xticklabels(xlabels)
    ax.set_ylim(0,1)

    resultFile.write("\nAverage accuracy: "+str(np.average(accuracyResult))+"\n")
    resultFile.write("Average Precision: "+str(np.average(precisionResult))+"\n")
    resultFile.write("Average Recall: "+ str(np.average(recallResult))+"\n")
    resultFile.write("Total Confusion matrix: \n["+str(totalConfusion[0][0])+","+ str(totalConfusion[0][1])+"] \n"+"["+str(totalConfusion[1][0])+","+ str(totalConfusion[1][1])+"] \n")
    resultFile.close()
    #print(cross_val_score(estimator=rf, X=features, y=labels, cv=skf, scoring="accuracy"))
    plt.savefig(resultFolder+"boxplotMeasures.png")
    #plt.show()
   
if __name__ == '__main__':
    
    if(sys.argv[1] == "y"):
        inputFile = 'finalDataSample.csv'
        randomForest(folder='../../csv112/', inputFile=inputFile)
    elif(sys.argv[1] == "n"):
        randomForest()
