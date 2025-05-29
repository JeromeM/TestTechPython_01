# XXXXX Technical Test

To run the application:

1. Install dependencies: `pip install -r requirements.txt`
2. Update currency rates: `python cli.py`
3. Start the FastAPI server: `uvicorn app.main:app --reload`

---
This implementation covers all the required tasks:

- A CLI to extract conversion rates from XML and store them in a SQLite database
- A parser using PLY to interpret currency conversion queries
- A converter to perform currency conversions using rates from the database
- A FastAPI-based REST web service that handles conversion requests

---
The architecture is modular and follows best practices:

- Separation of concerns (database, models, API routes, conversion logic)
- Use of dependency injection for database sessions
- Error handling and input validation
- Easily extensible for additional features

---
To improve this further, I could have added:

- More comprehensive error handling and logging
- Authentication and rate limiting for the API
- Caching of frequently used conversion rates
- Scheduled tasks to update rates automatically
