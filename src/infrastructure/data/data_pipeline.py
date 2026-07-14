import pandas as pd





class DataCleaner:
    """
    Pandas kullanarak eksik verileri dolduran,
     tarih formatlarını düzenleyen ve
      mükerrer kayıtları temizleyen veri mühendisliği sınıfı.
    """

    def __init__ (self, df):
        self.df = df

    def arrange_dates(self):
        self.df['Date'] = pd.to_datetime(self.df['Date'], format = '%d.%m.%Y')

    def fill_null_values(self):
        numerical_cols = self.df.select_dtypes(include = 'number').columns
        categorical_cols = self.df.select_dtypes(include = ['object', 'category']).columns

        self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].median()) #fill numerics with median
        self.df[categorical_cols] = self.df[categorical_cols].fillna('Unknown') #fill strings with 'Unknown'




