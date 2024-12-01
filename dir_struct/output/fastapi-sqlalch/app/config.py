from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True

settings = Settings()
