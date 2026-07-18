import pandas as pd
from dataclasses import asdict

class TransactionService:
    """
    This class gets transaction lists from repository, filters and returns the needed dataframe
    """

    def __init__(self, repo):
        self.repo = repo

    def _get_base_dataframe(self):
        transactions = self.repo.get_all_transactions()
        if not transactions:
            return pd.DataFrame()
        return pd.DataFrame([asdict(data) for data in transactions])

    def get_all_transactions(self):
        return self._get_base_dataframe()

    def get_expenses(self):
        df = self._get_base_dataframe()
        if df.empty: return df
        return df[df['amount'] < 0].reset_index(drop = True)

    def get_incomes(self):
        df = self._get_base_dataframe()
        if df.empty: return df
        return df[df['amount'] > 0].reset_index(drop = True)
