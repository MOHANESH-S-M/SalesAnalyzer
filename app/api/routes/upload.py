from fastapi import APIRouter, UploadFile, File,HTTPException
import pandas as pd
from app.services.data_processor import process_sales_data

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    # Process the uploaded file here
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    process_sales_data(file.file, )  # Replace None with your actual database session
    df = pd.read_csv(file.file)
    req_cols = ['Date', 'Product', 'Quantity', 'Price']
    if not all(col in df.columns for col in req_cols):
        raise HTTPException(status_code=400, detail=f"CSV must contain the following columns: {', '.join(req_cols)}")
    
    
@router.get("/")
async def read_root():
    return {"message": "Upload endpoint is working!"}