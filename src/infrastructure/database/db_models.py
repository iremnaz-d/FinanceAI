from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import String
from src.domain.entities import Category


class Base(DeclarativeBase):
    pass


class SQLAlchemyTransaction(Base):
    """
    This module is an SQLAlchemy ORM (Object-Relational-Mapping) class which
    defines schemas and corresponders of SQLite table of transactions
    """

    __tablename__ = "transactions"

    date = Mapped[datetime]
    id = Mapped[str] = mapped_column(primary_key = True) #Transaction ID as primary key
    description = Mapped[str] = mapped_column(String(150)) #varchar(50)
    amount = Mapped[float]
    balance = Mapped[float]
    category = Mapped[Optional[Category]]


