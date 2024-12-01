from fastapi import FastAPI
from .api.v1 import endpoints
from .database import engine
from .models.models import Base

app = FastAPI(title="High Performance FastAPI App")

# Include routers
app.include_router(endpoints.router, prefix="/api/v1", tags=["v1"])

# Create database tables
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # Uncomment the next line to drop all tables and recreate them
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "High Performance FastAPI with MySQL"}