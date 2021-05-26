  
import sys
import nltk
nltk.download(['punkt', 'wordnet'])
nltk.download('stopwords')
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import pickle

def load_data(database_filepath):
    """Load processed data from .db file.
    Arguments:
        database_filepath {str} -- rel. filepath to .db file
    """
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql("SELECT * FROM Messages", engine)
    X = df['message']
    Y = df.drop(columns=['id', 'genre', 'message', 'original'])
    category_names = Y.columns

    return X, Y, category_names

def tokenize(text):
    """Clean text to be used in ML algorithm.
    Arguments:
        text {str} -- text to be cleaned
    """
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

       
    clean_tokens = []
    for tok in tokens:
        if tok not in stopwords.words("english"):
            clean_tok = lemmatizer.lemmatize(tok).lower().strip()
            clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    """Build ML model using sklearn's pipeline module."""
    pipeline = Pipeline([
            ('vect', CountVectorizer(tokenizer=tokenize)),
            ('tfidf', TfidfTransformer()),
            ('clf', MultiOutputClassifier(RandomForestClassifier()))
        ])
    
    parameters = {
    'vect__ngram_range': [(1, 1)],
    'clf__estimator__min_samples_split': [2],
    }

    model = GridSearchCV(pipeline, param_grid=parameters, n_jobs=4, verbose=2)

    return model

def evaluate_model(model, X_test, Y_test, category_names):
    """Evaluate the ML learning model created using pipeline feature."""
    Y_pred = model.predict(X_test)
    
    for i in range(Y_pred.shape[1]):
        print('{}: ___________________________________'.format(category_names[i]))
        # report = classification_report(Y_pred[:,i], Y_test.values[:,i], target_names=category_names)
        # print(report)
        print(classification_report(Y_test, Y_pred, target_names=category_names))
        
    


def save_model(model, model_filepath):
    """Save trained model back as pickle string for use in webapp."""
    with open(model_filepath, 'wb') as file:
        pickle.dump(model, file)


def main():
    """Call function called to train classifier."""
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