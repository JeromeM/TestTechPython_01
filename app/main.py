from fastapi import FastAPI
from .api import routes
from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)