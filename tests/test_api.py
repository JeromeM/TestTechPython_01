from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import CurrencyRate
from datetime import date

client = TestClient(app)

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


def override_get_db():
    return MockDB()

app.dependency_overrides[get_db] = override_get_db

def test_convert_valid_query():
    response = client.get("/money/convert?query=10%20EUR%20to%20USD")
    assert response.status_code == 200
    assert response.json() == {"answer": "10.0 EUR = 11.0 USD"}

def test_convert_missing_query():
    response = client.get("/money/convert")
    assert response.status_code == 400
    assert "Query parameter is required" in response.text

def test_convert_invalid_query():
    response = client.get("/money/convert?query=invalid")
    assert response.status_code == 400

def test_convert_unsupported_currency():
    response = client.get("/money/convert?query=10%20XYZ%20to%20USD")
    assert response.status_code == 400
    assert "Unsupported currency: XYZ" in response.json()['detail']