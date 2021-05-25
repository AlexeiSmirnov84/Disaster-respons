import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """Load and combine two .csv files provided on id column.
        Arguments:
            messages_filepath {str} -- file path to messages .csv
            categories_filepath {str} -- filepath to categories .csv
        Returns:
            pd.DataFrame -- df containing csvs merged on id
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.concat([messages, categories], axis=1, join="inner")
    
    return df

def clean_data(df):
    """Split single string into 36 individual category columns.
        Arguments:
            df {pd.DataFrame} -- original dataframe
        Returns:
            pd.DataFrame -- df with categories split into columns
    """
    categories = df['categories'].str.split(pat=';', expand=True)
    row = categories.iloc[0,:]
    category_colnames = row.apply(lambda x: x[:len(x) - 2])
    categories.columns = category_colnames
    
    for column in categories:
        categories[column] = categories[column].apply(lambda x: x[len(x) - 1:])
        categories[column] = categories[column].astype(str)
      
    df = df.drop(['categories'], axis=1)
    df = pd.concat([df, categories], axis=1)
    df = df.drop_duplicates()

    return df
    
def save_data(df, database_filename):
    """Save cleaned data back into .db file.
        Arguments:
            df {pd.DataFrame} -- cleaned data
            database_path {str} -- complete relative file path of where file
            to be saved
    """
    engine = create_engine('sqlite:///'+database_filename)
    df.to_sql('Messages', engine, if_exists='replace', index=False)
    
def main():
    """Perform ETL tasks and providing user feedback."""
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