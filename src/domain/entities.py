from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots = True) #sonradan attribute eklemek istersem slotsu silicem
class Transaction:
    """
    Dataclass, holding bank account transactions' basic features
    """
    date: datetime
    id: str
    description: str
    amount: float
    balance: float
    category : Optional[Category]  = None

@dataclass
class Category:
    """
    Holds Transaction's category names and/or budget limits (basically category features)
    """
    name : str
    budget_limit = Optional[float] = None

