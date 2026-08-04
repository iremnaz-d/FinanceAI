import pandas as pd
from dataclasses import asdict
import streamlit as st

class TransactionService:
    """
    This class gets transaction lists from repository, filters and returns the needed dataframe
    """

    def __init__(self, repo):
        self.repo = repo

    @st.cache_data
    def _get_base_dataframe(_self):
        transactions = _self.repo.get_all_transactions()
        if not transactions:
            return pd.DataFrame()
        return pd.DataFrame([asdict(data) for data in transactions])

    @st.cache_data
    def get_all_transactions(_self):
        return _self._get_base_dataframe()

    @st.cache_data
    def get_expenses(_self):
        df = _self._get_base_dataframe()
        if df.empty: return df
        return df[df['amount'] < 0].reset_index(drop = True)

    @st.cache_data
    def get_incomes(_self):
        df = _self._get_base_dataframe()
        if df.empty: return df
        return df[df['amount'] > 0].reset_index(drop = True)
