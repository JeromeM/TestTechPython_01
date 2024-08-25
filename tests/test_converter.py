import pytest
from sqlalchemy.orm import Session
from app.conversion.converter import convert_currency, get_latest_rate
from app.models import CurrencyRate
from datetime import date

class MockDB:
    def query(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def first(self):
        return CurrencyRate(currency='USD', rate=1.1, date=date.today())
    
    def all(self):
        return [('USD',), ('EUR',), ('GBP',), ('JPY',)]  # Just simulate a list of supported currencies

    def distinct(self):
        return self

@pytest.fixture
def mock_db():
    return MockDB()

def test_get_latest_rate(mock_db):
    rate = get_latest_rate(mock_db, 'USD')
    assert rate.currency == 'USD'
    assert rate.rate == 1.1

def test_convert_currency_eur_to_usd(mock_db):
    result = convert_currency(mock_db, 10, 'EUR', 'USD')
    assert result == 11.00

def test_convert_currency_usd_to_eur(mock_db):
    result = convert_currency(mock_db, 11, 'USD', 'EUR')
    assert result == 10.00

def test_convert_currency_unavailable_rate(mock_db):
    mock_db.first = lambda: None
    with pytest.raises(ValueError, match="Rate not available for USD"):
        convert_currency(mock_db, 10, 'EUR', 'USD')