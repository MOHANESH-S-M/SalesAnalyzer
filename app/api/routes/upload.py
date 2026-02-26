from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    # Process the uploaded file here
    contents = await file.read()
    print(f"Received file: {file.filename}, content type: {file.content_type}, size: {len(contents)} bytes")
    return {"filename": file.filename, "content_type": file.content_type}

@router.get("/")
async def read_root():
    return {"message": "Upload endpoint is working!"}