from dataclasses import asdict

import plotly.express as px
import pandas as pd
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository





class FinancialVisualizer:
    """
    FinancialVisualizer: Plotly veya Matplotlib kullanarak pasta grafikleri,
    harcama trend çizgileri ve kategori dağılımlarını çizen arayüz sınıfı.
    """
    def __init__(self, df):
        self.df = df

    def plot_daily_trend(self,df):
        df1 = df.groupby('date')['amount'].sum()
        figure = px.line(df1, x='date', y='amount')
        figure.show()




"""if __name__ == '__main__':
     repo = SQLiteTransactionRepository(db=DataBaseSession())
     transaction_list = repo.get_all_transactions()
     df = pd.DataFrame([asdict(data) for data in transaction_list])

     vis = FinancialVisualizer(df)

     vis.plot_daily_trend(df) """



