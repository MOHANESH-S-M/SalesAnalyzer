from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc
from app.models.base import Sales

async def get_top_selling_products(db: AsyncSession, user_id: int, limit: int = 5):
    """Fetches the top selling products by quantity."""
    query = (
        select(
            Sales.product_name,
            func.sum(Sales.quantity).label("total_quantity")
        )
        .where(Sales.user_id == user_id)
        .group_by(Sales.product_name)
        .order_by(desc("total_quantity"))
        .limit(limit)
    )
    result = await db.execute(query)
    return result.all()

async def get_low_selling_products(db: AsyncSession, user_id: int, limit: int = 5):
    """Fetches the lowest selling products by quantity."""
    query = (
        select(
            Sales.product_name,
            func.sum(Sales.quantity).label("total_quantity")
        )
        .where(Sales.user_id == user_id)
        .group_by(Sales.product_name)
        .order_by(asc("total_quantity"))
        .limit(limit)
    )
    result = await db.execute(query)
    return result.all()

async def get_top_selling_categories(db: AsyncSession, user_id: int, limit: int = 5):
    """Fetches the top selling categories by quantity."""
    query = (
        select(
            Sales.category,
            func.sum(Sales.quantity).label("total_quantity")
        )
        .where(Sales.user_id == user_id)
        .group_by(Sales.category)
        .order_by(desc("total_quantity"))
        .limit(limit)
    )
    result = await db.execute(query)
    return result.all()

async def get_low_selling_categories(db: AsyncSession, user_id: int, limit: int = 5):
    """Fetches the lowest selling categories by quantity."""
    query = (
        select(
            Sales.category,
            func.sum(Sales.quantity).label("total_quantity")
        )
        .where(Sales.user_id == user_id)
        .group_by(Sales.category)
        .order_by(asc("total_quantity"))
        .limit(limit)
    )
    result = await db.execute(query)
    return result.all()

async def get_inventory_recommendations(db: AsyncSession, user_id: int, seasonality_factor: float = 1.0):
    """Generates basic inventory recommendations based on sales averages."""
    # 1. Get total sales per product
    query = (
        select(
            Sales.product_name,
            func.sum(Sales.quantity).label("total_quantity")
        )
        .where(Sales.user_id == user_id)
        .group_by(Sales.product_name)
    )
    result = await db.execute(query)
    products = result.all()

    if not products:
        return []

    # 2. Calculate average sales across all products
    total_volume = sum(p.total_quantity for p in products)
    avg_sales = total_volume / len(products) if products else 0

    # 3. Classify products
    recommendations = []
    for p in products:
        # Apply seasonality factor to project future demand
        projected_sales = p.total_quantity * seasonality_factor
        
        status = "Maintain Stock"
        priority = "Normal"
        
        if projected_sales >= avg_sales * 1.5:
            status = "High Demand - Restock Soon"
            priority = "High"
        elif projected_sales <= avg_sales * 0.5:
            status = "Low Demand - Consider Promotion/Clearance"
            priority = "Low"
            
        recommendations.append({
            "product_name": p.product_name,
            "total_sold": p.total_quantity,
            "projected_sales": round(projected_sales, 2),
            "recommendation": status,
            "priority": priority
        })
    
    # Sort by priority (High demand first) using projected sales
    recommendations.sort(key=lambda x: x['projected_sales'], reverse=True)
    return recommendations