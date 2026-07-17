import pandas as pd





class DataCleaner:
    """
    This class format dates and fill null values
    (categories with 'Unknown', numerics with median())
    """

    def __init__ (self, df):
        self.df = df

    def arrange_dates(self):
        self.df['date'] = pd.to_datetime(self.df['date'], format = '%d.%m.%Y', errors = 'coerce')
        self.df.dropna(subset=['date'], inplace=True)

    def fill_null_values(self):
        self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
        self.df['balance'] = pd.to_numeric(self.df['balance'], errors='coerce')

        numerical_cols = self.df.select_dtypes(include = 'number').columns
        categorical_cols = self.df.select_dtypes(include = ['object', 'category']).columns

        self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].median()) #fill numerics with median
        self.df[categorical_cols] = self.df[categorical_cols].fillna('Unknown') #fill strings with 'Unknown'




