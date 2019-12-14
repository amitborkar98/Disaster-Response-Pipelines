import sys
import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from sqlalchemy import create_engine
import pickle

nltk.download(['punkt', 'wordnet','stopwords'])

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report,accuracy_score, precision_score, recall_score, f1_score, make_scorer
from sklearn.model_selection import GridSearchCV


def load_data(database_filepath):
    '''
    Load data from the database
    Input:
        (File Path) database_filepath: File path of sql database
    Output:
        (DataFrame)X: Message (features)
        (DataFrame)Y: Categories (target)
        (List)category_names: Labels for 36 categories
    '''
    # Load data from database
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql("SELECT * FROM disaster_messages", engine)
    
    # Create X and Y datasets
    X = df['message']
    Y = df.drop(['id', 'message', 'original', 'genre'], axis = 1)
    
    # Create list containing all category names
    category_names = list(Y.columns.values)
    
    return X, Y, category_names        


def tokenize(text):
    """
    Tokenize the input text and return a cleaned token after lemmatization, stop-word removal, punctuation removal
    Inputs:
        (User Input) text: text input
    Outputs:
        (List) cleaned_tokens: list of cleaned tokens
    """
    #coverting into lower text
    text = text.lower() 
    
    #removing punctuations and other
    text = re.sub(r"[^a-zA-Z0-9]", " ", text) 
    
    #tokenizing words
    words = word_tokenize(text)
    
    #removing stopwords
    words_cleaned = [w for w in words if w not in stopwords.words("english")]
    
    #lematizing
    lemmatizer = WordNetLemmatizer()
    cleaned_tokens = []
    for tok in words_cleaned:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        cleaned_tokens.append(clean_tok)
    
    return cleaned_tokens
    
    
def build_model():
    '''
    Build a ML pipeline using Count Vectorizer, TF-IDF, AdaBoost Classifier and GridSearchCV
    Input: None
    Output:
        Result of GridSearchCV
    '''
    # Create pipeline
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer = tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(AdaBoostClassifier()))
        ])
    
    # Create parameters dictionary
    parameters = {  'vect__min_df': [1, 5],
                    'tfidf__use_idf':[True, False],
                    'clf__estimator__n_estimators': [50,100,150]}
    
    # Create grid search object
    cv = GridSearchCV(pipeline, param_grid=parameters)
    return cv

    
def evaluate_model(model, X_test, Y_test, category_names):
    """
    Output precision, recall, fscore for all the categories for test set
    Inputs:
        model: a trained model
        X_test: features of test set
        Y_test: target values of test set
        category_names: Labels for 36 categories
    Outputs: None
    """
    # Predict on test set 
    Y_pred = model.predict(X_test)
    # Calculate the overall accuracy of the model
    Overall_acc = (Y_pred == Y_test).mean().mean()
    print('Overall accuracy {0:.2f}% \n'.format(Overall_acc*100))
        
    #Create classifiaction report for each column    
    Y_pred_DF = pd.DataFrame(Y_pred, columns = Y_test.columns)
    for column in Y_test.columns:
        print('****     *****     ***** \n')
        print('Feature Name: {}\n'.format(column))
        print(classification_report(Y_test[column],Y_pred_DF[column]))

        
def save_model(model, model_filepath):
    '''
    Save model as a pickle file 
    Input: 
        model: Model to be saved
        model_filepath: path of the output pick file
    Output:
        A pickle file of saved model
    '''
    #save the model as pickle file
    pickle.dump(model, open(model_filepath, "wb"))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()