import pandas as pd

from src.infrastructure.data.data_pipeline import DataCleaner


class ExcellReader:
    """
    Bankalardan gelen farklı CSV formatlarını okuyan ve
     ham veriyi standart veri sözlüklerine dönüştüren yardımcı sınıf.
    """

    def __init__ (self, path):
        self.path = path # r"C:\Users\irem naz\Desktop\FinanceAI\src\data\Transaction_History.xlsx"

    def read(self):
        df = pd.read_excel(self.path)
        df.drop(index=df.index[:11], inplace=True)
        df.columns = ['Date', 'ID', 'Description', 'Amount', 'Balance']

        cleaner = DataCleaner(df=df)
        cleaner.arrange_dates()
        cleaner.fill_null_values()
        return cleaner.df

"""reader = ExcellReader(r"C:\Users\irem naz\Desktop\FinanceAI\src\data\Transaction_History.xlsx")
df = reader.read()
with pd.option_context('display.max_columns', None):
 print(df.head(15))"""