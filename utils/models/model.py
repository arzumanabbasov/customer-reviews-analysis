import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Modeling:
    """
    This class applies the VADER sentiment analysis tool to the text data and adds the results to the dataframe. The
    class takes a pandas dataframe as input and assigns it to the df attribute. The class has a method called train that
    applies the VADER sentiment analysis tool to the text data and adds the results to the dataframe. The class also has
    a method called evaluate that evaluates the model. The class also has a method called predict that takes new data as
    input and returns the sentiment scores. The class also has a method called run that returns the dataframe.


    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    def __init__(self, df: pd.DataFrame):
        """
        This method initializes the class with a pandas dataframe. The method takes a pandas dataframe as input and
        assigns it to the df attribute.
        :param df: pd.DataFrame
        """
        self.df = df
        self.sid = SentimentIntensityAnalyzer()

    def apply_vader(self, text: pd.Series):
        """
        This method applies the VADER sentiment analysis tool to the text data and returns the sentiment scores.
        :param text:
        :return text:
        """
        return text.apply(lambda x: self.sid.polarity_scores(x))

    def train(self):
        """
        This method applies the VADER sentiment analysis tool to the text data and adds the results to the dataframe.
        :return: None
        """
        sentiment = self.apply_vader(self.df['text'])
        self.df['compound'] = sentiment.apply(lambda x: x['compound'])
        self.df['neg'] = sentiment.apply(lambda x: x['neg'])
        self.df['neu'] = sentiment.apply(lambda x: x['neu'])
        self.df['pos'] = sentiment.apply(lambda x: x['pos'])

    def evaluate(self):
        # Add your evaluation logic here
        pass

    def predict(self, new_data):
        sentiments = self.apply_vader(new_data)
        return sentiments

    def run(self):
        return self.df

