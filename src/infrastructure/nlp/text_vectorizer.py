from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin

class TextVectorizer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit(self, X, y = None):
        """
        :param X: Only 'description' column from train_x
        :param y: None
        :return: TextVectorizer
        """
        self.vectorizer.fit(X)
        return self

    def transform(self, X, y = None):
        """
        :param X: only 'description' column from test_x
        :param y: None
        :return: TextVectorizer
        """
        return self.vectorizer.transform(X)


