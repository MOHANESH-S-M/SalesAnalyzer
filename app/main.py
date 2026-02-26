from fastapi import FastAPI,APIRouter
from app.api.api_router import api_router
app = FastAPI()

app.include_router(api_router, prefix="")
@app.get("/")
def root():
    return {"message":"project started"}