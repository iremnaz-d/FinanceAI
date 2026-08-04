import os


class Settings:


    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    db_path = os.path.join(base_dir, 'finance_app.db').replace('\\', '/')

    DATABASE_URL = f"sqlite:///{db_path}"
    FILE_PATH = r"C:\Users\irem naz\Desktop\FinanceAI\src\data\Transaction_History.xlsx"

    REGEX_DESCRIPTION = [r'\d+',
                         r'\bsanal\b',
                         r'\bPOS\b',
                         r'\balışveriş\b',
                         r'\bkart\b',
                         r'\bno\b',
                         r'\byurtiçi\b',
                         r'\bmutabakat\b',
                         r'[^\w\s]']