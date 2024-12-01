from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ...database import get_db
from ...models.models import Products, Categories, Customers, Orders, OrderItems
from ...schemas.base import (
    ProductCreate, ProductResponse,
    CategoryCreate, CategoryResponse,
    CustomerCreate, CustomerResponse
)

router = APIRouter()

@router.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    db_product = Products(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.get("/products/", response_model=List[ProductResponse])
async def get_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(Products).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/categories/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    db_category = Categories(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.get("/categories/", response_model=List[CategoryResponse])
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(Categories).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()