from sqlalchemy.orm import Session
from sqlalchemy import distinct
from app.models import CurrencyRate
from datetime import date
import logging

# Get supported currencies from DB
def get_supported_currencies(db: Session):
    currencies = [currency[0] for currency in db.query(distinct(CurrencyRate.currency)).all()]
    currencies.append('EUR')
    return currencies

def get_latest_rate(db: Session, currency: str):
    # There are some days with no conversion rates.. We will search the latest
    return db.query(CurrencyRate).filter(CurrencyRate.currency == currency).order_by(CurrencyRate.date.desc()).first()

def convert_currency(db: Session, amount: float, from_currency: str, to_currency: str):
    # The function can convert from and to EUR
    logging.debug(f"Converting {amount} from {from_currency} to {to_currency}")

    # Check if currencies are supported
    supported_currencies = get_supported_currencies(db)
    logging.debug(supported_currencies)
    if from_currency not in supported_currencies or to_currency not in supported_currencies:
        raise ValueError(f"Unsupported currency: {from_currency if from_currency not in supported_currencies else to_currency}")

    if from_currency == "EUR":
        to_rate = get_latest_rate(db, to_currency)
        if not to_rate:
            raise ValueError(f"Rate not available for {to_currency}")
        logging.debug(f"Latest {to_currency} rate: {to_rate.rate} (date: {to_rate.date})")
        return round(amount * to_rate.rate, 2)
    
    if to_currency == "EUR":
        from_rate = get_latest_rate(db, from_currency)
        if not from_rate:
            raise ValueError(f"Rate not available for {from_currency}")
        logging.debug(f"Latest {from_currency} rate: {from_rate.rate} (date: {from_rate.date})")
        return round(amount / from_rate.rate, 2)
    
    # Everything that is not EUR (neither from and to)
    from_rate = get_latest_rate(db, from_currency)
    to_rate = get_latest_rate(db, to_currency)

    if not from_rate or not to_rate:
        raise ValueError("Currency rates not available")

    logging.debug(f"Latest {from_currency} rate: {from_rate.rate} (date: {from_rate.date})")
    logging.debug(f"Latest {to_currency} rate: {to_rate.rate} (date: {to_rate.date})")

    result = (amount / from_rate.rate) * to_rate.rate
    return round(result, 2)