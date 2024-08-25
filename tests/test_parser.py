import pytest
from app.conversion.parser import parse_query

def test_parse_query_valid():
    query = "10.32 EUR to USD"
    result = parse_query(query)
    assert result == {'amount': 10.32, 'from_currency': 'EUR', 'to_currency': 'USD'}

def test_parse_query_invalid_format():
    with pytest.raises(ValueError):
        parse_query("invalid query")

def test_parse_query_invalid_amount():
    with pytest.raises(ValueError):
        parse_query("abc EUR to USD")

def test_parse_query_missing_to():
    with pytest.raises(ValueError):
        parse_query("10.32 EUR USD")

def test_parse_query_invalid_currency():
    with pytest.raises(ValueError):
        parse_query("10.32 EU to US")