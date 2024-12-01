from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func

Base = declarative_base()

# This will be the base for all generated models
class BaseModel(Base, AsyncAttrs):
    __abstract__ = True
    
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"