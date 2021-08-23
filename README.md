# Regenwateroverlast
With this git repo it is possible to create a dataset for the rainwater damage project. 

## Setup
1. set up a conda environnement with the requirements in ./requirements/requirements3.txt
    Osgeo and scikit learn have to be installed seperately in this conda environment.
2. Download the datasets. You may have to make some alterations to the filepaths in the python scripts used for preprocessing the data to make the filepaths there match your own filestructure. Do not save the raw data into the git repository as this data takes up too much storage and/or contains privacy sensitive information.
    1. KNMI data, source can be found in ./documentation/Manuals/KNMIdata.txt. Download the zip files from years you would like data on and extract them in a parent directory ../KNMI/ 
    2. AHN data, use the scripts in ./scripts to scrape the data and save files to ../AHN

## Subfolders
### ./preprocessing112
Contains all preprocessing steps to create a dataset with p2000 alerts as a target. Use ./preprocessing112/serialized.py (or one of the other serialized scripts when you want different rain features) to create the dataset.

### ./pandafy_data
Contains all preprocessing steps to create a dataset with twitter alerts as a target. Use ./pandafy_data/scripstSerialized.py to create the dataset.

### ./analyse112
Train and evaluate a model on p2000 data.

### ./analyseTwitter
Train an evaluate a model on twitter data

### ./documentation
Some additional resources, figures and the bachelor thesis

### ./experiments
Experiments and results used to work on ALICE.

### ./tifFiles
scripts to open .tiff files
