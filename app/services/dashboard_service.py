from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Sales

async def get_sales_line_graph(db: AsyncSession, user_id: int):
    """
    Line chart data: total revenue per day.
    Returns: [{ "date": "YYYY-MM-DD", "revenue": 1234 }, ...]
    """
    stmt = (
        select(
            Sales.date.label("date"),
            func.sum(Sales.selling_price * Sales.quantity).label("revenue")
        )
        .where(Sales.user_id == user_id)
        .group_by(Sales.date)
        .order_by(Sales.date.asc())
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [
        {"date": row.date.isoformat(), "revenue": float(row.revenue or 0)}
        for row in rows
    ]

async def get_sales_pie_chart(db: AsyncSession, user_id: int):
    """
    Pie chart data: total sales by category.
    Returns: [{ "category": "Category Name", "revenue": 1234 }, ...]
    """
    stmt = (
        select(
            Sales.category.label("category"),
            func.sum(Sales.selling_price * Sales.quantity).label("revenue")
        )
        .where(Sales.user_id == user_id)
        .group_by(Sales.category)
        .order_by(func.sum(Sales.selling_price * Sales.quantity).desc())
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [
        {"category": row.category, "revenue": float(row.revenue or 0)}
        for row in rows
    ]