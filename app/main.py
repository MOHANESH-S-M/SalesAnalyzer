from datetime import date
from fastapi import FastAPI
from sqlalchemy import select
from app.api.api_router import api_router
from app.db.session import AsyncSessionLocal
from app.models.base import Sales
import os

app = FastAPI()
app.include_router(api_router, prefix="")

@app.get("/")
def root():
    return {"message": "project started"}

@app.get("/check_db")
async def check_db_insertion():
    async with AsyncSessionLocal() as session:
        sale = Sales(
            product_name="test",
            quantity=10,
            selling_price=100,
            category="test",
            date=date(2024, 6, 1),
        )
        session.add(sale)
        await session.commit()
        await session.refresh(sale)
    return {"message": "Database check successful", "id": sale.id}

@app.get("/check_db_retrieve")
async def check_db_retrieve():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Sales).order_by(Sales.id.desc()).limit(5)
        )
        rows = result.scalars().all()
    return {
        "sales": [
            {
                "id": r.id,
                "product_name": r.product_name,
                "quantity": r.quantity,
                "selling_price": r.selling_price,
                "category": r.category,
                "date": r.date.isoformat(),
            }
            for r in rows
        ]
    }