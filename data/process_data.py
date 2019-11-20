import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    INPUT:
    messages_filepath - path to csv file containing messages
    categories_filepath - path to csv file containing categories
        
    OUTPUT:
    df - a joined dataframe containg messages and categories
    '''
    # Load Datasets
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    
    # Merge Datasets
    df = messages.merge(categories, on='id')

    return df

def clean_data(df):
    '''
    INPUT:
    df - merged dataset of messages and categories
        
    OUTPUT:
    df - cleaned data
    '''
    # Creating a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(';', expand=True)
    
    # Selecting the first row of the categories DataFrame, extracting the names of the categories and renaming the columns of the categories DataFrame
    row = categories.iloc[0,:]
    category_colnames = row.apply(lambda x: x[:-2])
    categories.columns = category_colnames

    # Converting the category values to just numbers 0 or 1
    for column in categories:
        categories[column] = categories[column].apply(lambda x : x[-1])
        categories[column] = categories[column].astype(int)
        
    # Dropping the original uncleaned categories column from the DataFrame df
    df.drop('categories', axis=1, inplace=True)
    
    # Concatenating the original DataFrame with the new categories DataFrame
    df = pd.concat([df,categories], axis=1)
    
    # Droping duplicates
    df.drop_duplicates(inplace=True)
    
    return df

def save_data(df, database_filename):
    pass  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()