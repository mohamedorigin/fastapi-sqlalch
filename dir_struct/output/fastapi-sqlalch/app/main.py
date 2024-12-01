from fastapi import FastAPI
from .api.v1 import endpoints

app = FastAPI(title="FastAPI Application")

app.include_router(endpoints.router, prefix="/api/v1")
