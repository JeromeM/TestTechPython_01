from sqlalchemy import Column, Float, String, Date
from .database import Base

class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(String, primary_key=True)
    currency = Column(String, index=True)
    rate = Column(Float)
    date = Column(Date)