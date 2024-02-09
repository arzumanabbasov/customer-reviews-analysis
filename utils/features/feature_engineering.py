import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')


class FeatureEngineering:
    """
    This class is responsible for cleaning and transforming the data from the database. It also saves the data to a
    csv file. The class has 3 methods: load, transform, and save. The load method reads the data from the database
    and stores it in a pandas dataframe. The transform method cleans the data and adds a sentiment column. The save
    method saves the data to a csv file. The run method calls the load, transform, and save methods in that order.
    The class takes 3 parameters: QUERY, connection, and filename. The QUERY parameter is a string that contains the
    SQL query to be executed. The connection parameter is the connection to the database. The filename parameter is
    the name of the csv file to be saved. The default value for the filename parameter is 'reviews'. The class uses
    the WordNetLemmatizer and the stopwords from the nltk library to clean the text data. The class also uses the
    pandas library to read and write the data.
    """

    def __init__(self, QUERY: str, connection, filename: str = 'reviews'):
        """
        This method is a constructor that initializes the class with the QUERY, connection, and filename parameters. The
        default value for the filename parameter is 'reviews'. The method also initializes the WordNetLemmatizer and the
        stopwords from the nltk library. The method takes 3 parameters: QUERY, connection, and filename. The QUERY
        parameter is a string that contains the SQL query to be executed. The connection parameter is the connection to
        the database. The filename parameter is the name of the csv file to be saved.

        :param QUERY: str
        :param connection: connection
        :param filename: str
        :return: None
        """
        self.query = QUERY
        self.conn = connection
        self.filepath = f'C://Users/Admin/Desktop/Projects/Customer_Pain_Point_Analysis/data/raw/{filename}.csv'
        self.df = None
        self.ls = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def textcleaner(self, text: pd.Series):
        """
        This method cleans the text data by removing email addresses, web addresses, money symbols, phone numbers,
        digits, non-word characters, and extra spaces. The method also converts the text to lowercase, removes stop
        words, and lemmatizes the words. The method takes a pandas series as input and returns a pandas series.

        :param text: pd.Series
        :return: pd.Series
        """
        processed = text.str.replace(r'^.+@[^\.].*\.[a-z]{2,}$', 'emailaddr')
        processed = processed.str.replace(r'^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$', 'webaddress')
        processed = processed.str.replace(r'£|\$', 'moneysymb')
        processed = processed.str.replace(r'^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$', 'phonenumbr')
        processed = processed.str.replace(r'\d+(\.\d+)?', 'numbr')
        processed = processed.str.replace(r'[^\w\d\s]', ' ')
        processed = processed.str.replace(r'\s+', ' ')
        processed = processed.str.replace(r'^\s+|\s+?$', '')
        processed = processed.str.lower()
        processed = processed.apply(lambda x: ' '.join(term for term in x.split() if term not in self.stop_words))
        processed = processed.apply(lambda x: ' '.join(self.ls.lemmatize(term) for term in x.split()))
        return processed

    def load(self):
        """
        This method reads the data from the database and stores it in a pandas dataframe. The method takes no parameters
        and returns a pandas dataframe.
        :return: pd.DataFrame
        """
        self.df = pd.read_sql_query(self.query, self.conn)
        return self.df

    def transform(self):
        """
        This method cleans the data and adds a sentiment column. The method takes no parameters and returns a pandas
        dataframe. Method also drops the 'id' column and the rows with a rating of -1. The method also adds a 'len'
        column that contains the length of the text.
        The method also adds a 'sentiment' column that contains a 1 for positive ratings and a 0 for negative
        ratings. The method also calls the textcleaner method to clean the text data. The method returns a pandas
        dataframe.

        :return: pd.DataFrame
        """
        print(self.df.date[0])
        self.df['date'] = self.df['date'].astype('str')
        self.df = self.df.drop(columns=['id'])
        self.df = self.df = self.df.drop(self.df[self.df['rating'] == -1].index)
        self.df['sentiment'] = np.where(self.df['rating'] > 3, 1, 0)  # 1 is positive, 0 is negative
        self.df['len'] = self.df['text'].apply(len)
        self.df['text'] = self.textcleaner(self.df['text'])
        return self.df

    def save(self):
        """
        This method saves the data to a csv file. The method takes no parameters and returns the filepath of the csv
        file. :return: str
        """
        self.df.to_csv(self.filepath, index=False)
        return self.filepath

    def run(self):
        """
        This method calls the load, transform, and save methods in that order. The method takes no parameters and
        returns the filepath of the csv file. :return: filepath: str
        """
        self.load()
        return self.transform()
