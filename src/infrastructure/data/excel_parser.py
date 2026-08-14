import pandas as pd
from src.infrastructure.data.data_pipeline import DataCleaner
from src.domain.entities import Transaction

class ExcelReader:
    """
    This class reads the raw data file, cleans the data, and returns a cleaned Transaction List
    """

    def __init__ (self, path):
        self.path = path # r"src/data/Transaction_History.xlsx"

    def read(self):
        try:
            df = pd.read_excel(self.path)
        except Exception as e:
            return str(e)

        # I'm specifically omitting the first 11 lines of raw data, this may vary from bank to bank
        df.drop(index=df.index[:11], inplace=True)
        df.columns = ['date', 'id', 'description', 'amount', 'balance']

        cleaner = DataCleaner(df=df)
        df1 =  cleaner.clean()

        transaction_list = [Transaction(
            date = row['date'],
            _id = row['id'],
            amount = row['amount'],
            description = row['description'],
            balance = row['balance'],
            category = ""
        ) for index, row in df1.iterrows()]

        return transaction_list