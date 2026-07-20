import pandas as pd

from src.infrastructure.ml.text_classifier import TextClassifier


class TransactionPredictor:

    def __init__(self, transaction_list):
        self.transaction_list = transaction_list

    def list_to_dataframe(self):
        column_names = ['date', 'id', 'description', 'amount', 'balance', 'category']
        return pd.DataFrame(self.transaction_list, columns = column_names)

    def split_data(self):
        df = self.list_to_dataframe()

        df_test = df[df['category'] == 'Other']
        df_train = df[df['category'] != 'Other']

        train_x = df_train[['amount', 'description']]
        train_y = df_train['category']
        train_ids = df_train['id']

        test_x = df_test[['amount', 'description']]
        test_y = df_test['category']
        test_ids = df_test['id']

        return train_x, train_y,train_ids, test_x, test_y, test_ids

    def predict_category(self):
        train_x, train_y,train_ids, test_x, test_y ,test_ids= self.split_data()
        classifier = TextClassifier()

        classifier.fit(train_x, train_y)
        predictions = classifier.predict(test_x)

        predicted_categories = dict(zip(test_ids, predictions))
        for transaction in self.transaction_list:
            if transaction.id in predicted_categories:
                transaction.category = f"{predicted_categories[transaction.id]} (Predicted)"

        return self.transaction_list
