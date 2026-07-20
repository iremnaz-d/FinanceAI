from sklearn.naive_bayes import MultinomialNB
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from src.infrastructure.nlp.text_vectorizer import TextVectorizer


class TextClassifier:

    def __init__(self):
        self.model_pipeline = None

    def fit(self, train_x, train_y):
        train_x = train_x.copy()
        train_x['amount'] = train_x['amount'].abs()

        preprocessor = ColumnTransformer(
            transformers = [
                ('text', TextVectorizer(), 'description'),
                ('num', 'passthrough', ['amount'])          #amount column passes as it is
            ]
        )

        self.model_pipeline = Pipeline(steps = [
            ('preprocessor', preprocessor),
            ('classifier', MultinomialNB())
        ])

        self.model_pipeline.fit(train_x, train_y)

    def predict(self, test_x):
        test_x = test_x.copy()
        test_x['amount'] = test_x['amount'].abs()
        return self.model_pipeline.predict(test_x)


