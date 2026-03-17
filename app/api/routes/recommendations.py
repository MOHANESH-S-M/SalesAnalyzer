from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies import get_current_user
from app.services.recommendation_service import (
    get_top_selling_products,
    get_low_selling_products,
    get_inventory_recommendations,
    get_top_selling_categories,
    get_low_selling_categories )

router = APIRouter()

def get_seasonal_factor() -> float:
    """Determine seasonality factor based on the current month."""
    current_month = datetime.now().month
    
    # Festive/Holiday Season (Oct, Nov, Dec) -> Increase forecast by 20%
    if current_month in [10, 11, 12]:
        return 1.2
    # Post-Holiday Slump (Jan, Feb) -> Decrease forecast by 10%
    elif current_month in [1, 2]:
        return 0.9
    # Standard demand for rest of the year
    return 1.0

@router.get("/top-sellers")
async def top_sellers(
    limit: int = 5, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Get top selling products."""
    user_id = current_user.id
    data = await get_top_selling_products(db, user_id, limit)
    return {"data": [{"product_name": row.product_name, "total_quantity": row.total_quantity} for row in data]}

@router.get("/low-sellers")
async def low_sellers(
    limit: int = 5, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Get lowest selling products."""
    user_id = current_user.id
    data = await get_low_selling_products(db, user_id, limit)
    return {"data": [{"product_name": row.product_name, "total_quantity": row.total_quantity} for row in data]}

@router.get("/categories/top-sellers")
async def top_categories(
    limit: int = 5, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Get top selling categories."""
    user_id = current_user.id
    data = await get_top_selling_categories(db, user_id, limit)
    return {"data": [{"category": row.category, "total_quantity": row.total_quantity} for row in data]}

@router.get("/categories/low-sellers")
async def low_categories(
    limit: int = 5, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Get lowest selling categories."""
    user_id = current_user.id
    data = await get_low_selling_categories(db, user_id, limit)
    return {"data": [{"category": row.category, "total_quantity": row.total_quantity} for row in data]}

@router.get("/inventory-recommendations")
async def inventory_recommendations(
    seasonality_factor: Optional[float] = None,
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Get inventory stock recommendations."""
    # If no factor provided, calculate based on current month
    if seasonality_factor is None:
        seasonality_factor = get_seasonal_factor()

    user_id = current_user.id
    data = await get_inventory_recommendations(db, user_id, seasonality_factor)
    return {"seasonality_factor": seasonality_factor, "recommendations": data}