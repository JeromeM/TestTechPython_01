from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.conversion.parser import parse_query
from app.conversion.converter import convert_currency
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)

@router.get("/money/convert")
def convert(query: str = Query(None, description="Conversion query string"), db: Session = Depends(get_db)):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    try:
        logging.debug(f"Received query: {query}")
        parsed_query = parse_query(query)
        logging.debug(f"Parsed query: {parsed_query}")
        result = convert_currency(db, parsed_query['amount'], parsed_query['from_currency'], parsed_query['to_currency'])
        logging.debug(f"Conversion result: {result}")
        return {"answer": f"{parsed_query['amount']} {parsed_query['from_currency']} = {result} {parsed_query['to_currency']}"}
    except ValueError as e:
        logging.error(f"ValueError occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")