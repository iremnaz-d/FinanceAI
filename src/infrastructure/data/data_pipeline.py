import pandas as pd
from src.config.settings import Settings

class DataCleaner:
    """
    This class format dates and fill null values
    (categories with 'Unknown', numerics with median())
    """

    def __init__ (self, df):
        self.df = df

    def clean(self):
        self.arrange_dates()
        self.fill_null_values()
        self.clean_descriptions()
        return self.df

    def arrange_dates(self):
        """
        Drops transactions with an empty date field and converts those with a value to the datetime format
        """
        self.df['date'] = pd.to_datetime(self.df['date'], format = '%d.%m.%Y', errors = 'coerce')
        self.df.dropna(subset=['date'], inplace=True)

    def fill_null_values(self):
        self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
        self.df['balance'] = pd.to_numeric(self.df['balance'], errors='coerce')

        numerical_cols = self.df.select_dtypes(include = 'number').columns
        categorical_cols = self.df.select_dtypes(include = ['object', 'category']).columns

        self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].median()) #fill numerics with median
        self.df[categorical_cols] = self.df[categorical_cols].fillna('Unknown') #fill strings with 'Unknown'

    def clean_descriptions(self):
        regex_list = Settings.REGEX_DESCRIPTION
        regex_description = r'(' + '|'.join(regex_list) + r')'

        self.df['description'] = self.df['description'].str.replace(regex_description, "  ", case = False, regex = True)
        self.df['description'] = self.df['description'].str.replace(r'\s+',' ', regex = True).str.strip()








