from fastapi import APIRouter, UploadFile, File,HTTPException, Depends
from app.services.data_processor import process_sales_data
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), 
                      current_user = Depends(get_current_user)):
    """Endpoint to upload a CSV file containing sales data."""
    print(f"Received file: {file.filename}")
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    return await process_sales_data(file.file, db, current_user.id)
    
@router.get("/")
async def read_root():
    return {"message": "Upload endpoint is working!"}