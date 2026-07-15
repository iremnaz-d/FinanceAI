from dataclasses import dataclass
from datetime import datetime

@dataclass(slots = True) #sonradan attribute eklemek istersem slotsu silicem
class Transaction:
    """
    Transaction: Benzersiz ID, tarih, açıklama, miktar ve
    kategori bilgilerini tutan saf Python veri sınıfı (dataclass)
    """
    date: datetime
    id: str
    description: str
    amount: float
    balance: float

class Category:
    """
    Category: Kategorilerin adlarını ve bütçe limitlerini tanımlayan temel nesne sınıfı.
    """