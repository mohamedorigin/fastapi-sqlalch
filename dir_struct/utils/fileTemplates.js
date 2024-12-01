const templates = {
  'requirements.txt': `fastapi
sqlalchemy
alembic
pydantic
psycopg2-binary
python-dotenv
`,
  'alembic.ini': `# alembic configuration
sqlalchemy.url = postgresql://user:password@localhost/dbname
`,
  '__init__.py': '',
  'base.py': `from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
`,
  'database.py': `from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
`,
  'config.py': `from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True

settings = Settings()
`,
  'main.py': `from fastapi import FastAPI
from .api.v1 import endpoints

app = FastAPI(title="FastAPI Application")

app.include_router(endpoints.router, prefix="/api/v1")
`,
  'endpoints.py': `from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}
`,
  'env.py': `from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config
fileConfig(config.config_file_name)
`
};

export default templates;