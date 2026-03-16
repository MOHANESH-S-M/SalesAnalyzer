from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies import get_current_user
from app.services.recommendation_service import (
    get_top_selling_products,
    get_low_selling_products,
    get_inventory_recommendations )

router = APIRouter()

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

@router.get("/inventory-recommendations")
async def inventory_recommendations(
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Get inventory stock recommendations."""
    user_id = current_user.id
    data = await get_inventory_recommendations(db, user_id)
    return {"recommendations": data}