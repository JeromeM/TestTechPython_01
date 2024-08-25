import click
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, CurrencyRate

@click.command()
def update_rates():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    # Not working without namespaces..
    namespaces = {
        'gesmes': 'http://www.gesmes.org/xml/2002-08-01',
        'ecb': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'
    }
    response = requests.get(url)
    root = ET.fromstring(response.content)

    rates = {}
    date = None
    # Get all Cubes with time, to be sure to use the latest
    for cube in root.findall('.//ecb:Cube[@time]', namespaces):
        date = datetime.strptime(cube.attrib['time'], '%Y-%m-%d').date()
        for rate in cube.findall('ecb:Cube', namespaces):
            currency = rate.attrib['currency']
            rate_value = float(rate.attrib['rate'])
            rates[currency] = rate_value

    db = SessionLocal()
    try:
        for currency, rate in rates.items():
            db_rate = CurrencyRate(id=f"{date}_{currency}", currency=currency, rate=rate, date=date)
            db.merge(db_rate)
        db.commit()
        click.echo(f"Updated {len(rates)} currency rates for {date}")
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    update_rates()