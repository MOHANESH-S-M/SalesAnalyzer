from fastapi import APIRouter, UploadFile, File,HTTPException , Depends
from app.services.dashboard_service import get_sales_line_graph, get_sales_pie_chart
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/sales/line-graph")
async def line_graph(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """Endpoint to get line graph data for sales."""
    user_id = current_user.id
    data = await get_sales_line_graph(db, user_id)
    if not data:
        raise HTTPException(status_code=404, detail="No sales data found for line graph.")
    return {"line_graph_data": data}

@router.get("/sales/pie-chart")
async def pie_chart(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """Endpoint to get pie chart data for sales."""
    user_id = current_user.id
    data = await get_sales_pie_chart(db, user_id)
    if not data:
        raise HTTPException(status_code=404, detail="No sales data found for pie chart.")
    return {"pie_chart_data": data}