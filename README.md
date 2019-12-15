# Disaster Response Pipeline Project

### Installation:
The code contained in this repository was written in HTML and Python 3, and requires the following Python packages: json, plotly, pandas, nltk, flask, sklearn, sqlalchemy, sys, numpy, pickle.

### Project Overview:
This repository contains code for a web app which an emergency worker could use during a disaster event (e.g. an earthquake or hurricane), to classify a disaster message into several categories, in order that the message can be directed to the appropriate aid agencies.

The app uses a ML model to categorize any new messages received, and the repository also contains the code used to train the model and to prepare any new datasets for model training purposes.

I have first created a ETL pipeline-process_data.py by cleaning and wrangling the two datasets and finally merging it.Then i have created a ML model-
train_classifier.py and saved it in a pickle file-classifier.pkl.

### Files:
1)models : This folder contains train_classifier.py script and classifier.pkl model.
2)data: This folder contains sample messages and categories datasets in csv format and the sqlite database file.
3)app: This folder contains all of the files necessary to run and render the web app.

### Warning:
The datasets included in this repository are very unbalanced, with very few positive examples for several message categories. In some cases, the proportion of positive examples is less than 5%, or even less than 1%. In such cases, even though the classifier accuracy is very high (since it tends to predict that the message does not fall into these categories), the classifier recall (i.e. the proportion of positive examples that were correctly labelled) tends to be very low. As a result, care should be taken if relying on the results of this app for decision making purposes.

### Results:
AdaBoost classifier is used to predict the categories.The model predicts the test set with 94.70% accuracy.

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
