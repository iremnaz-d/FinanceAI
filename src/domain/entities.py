from dataclasses import dataclass
from datetime import datetime
from typing import Optional

#from src.infrastructure.database.db_models import SQLAlchemyTransaction


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

    def __init__(self, date:datetime, _id:str,description:str, amount:float, balance:float, category:Category = None):
        self.date  = date
        self.id = _id
        self.description = description
        self.amount = amount
        self.balance = balance


    @classmethod
    def from_db_model(cls, db_model):
        """
        converts SQLAlchemyTransaction to corresponding domain Transaction
        :param db_model: SQLAlchemyTransaction
        :return: Transaction
        """

        return cls(
            date = db_model.date,
            _id = db_model.id,
            description = db_model.description,
            amount = db_model.amount,
            balance = db_model.balance
        )

    @classmethod
    def from_db_model_plural(cls, db_model_list: list[SQLAlchemyTransaction]):
        """
        :param db_model_list: SQLAlchemyTransaction list
        :return: Transaction list
        """


        _list = []
        for model in db_model_list:
            _list.append(cls.from_db_model(db_model = model))
        return _list



@dataclass
class Category:
    """
    Holds Transaction's category names and/or budget limits (basically category features)
    """
    name : str
    budget_limit : Optional[float] = None

