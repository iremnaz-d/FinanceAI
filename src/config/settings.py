import os


class Settings:


    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

    DATABASE_URL = f"sqlite:///{os.path.join(base_dir, 'finance_app.db')}"
    FILE_PATH = r"C:\Users\irem naz\Desktop\FinanceAI\src\data\Transaction_History.xlsx"

    REGEX_DESCRIPTION = [r'\d+', 'sanal','POS', 'alışveriş','kart', 'no','yurtiçi','mutabakat',
                         r'[^\w\s]']