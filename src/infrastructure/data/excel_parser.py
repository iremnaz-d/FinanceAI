import pandas as pd

from src.infrastructure.data.data_pipeline import DataCleaner


class ExcellReader:
    """
    Bankalardan gelen farklı CSV formatlarını okuyan ve
     ham veriyi standart veri sözlüklerine dönüştüren yardımcı sınıf.
    """

    def __init__ (self, path):
        self.path = path

    df = pd.read_excel(r"C:\Users\irem naz\Desktop\FinanceAI\src\data\Transaction_History.xlsx")
    df.drop(index = df.index[:11], inplace = True)
    df.columns = ['Date', 'Transaction ID', 'Description', 'Amount', 'Balance']

    cleaner = DataCleaner(df = df)
    cleaner.fill_null_values()
    cleaner.arrange_dates()

    print(df.head(15))