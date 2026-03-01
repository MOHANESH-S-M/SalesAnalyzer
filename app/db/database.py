
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL= "postgresql+asyncpg://postgres:ZSpRRcts4srjAO2V@db.wsotoictjsadbwspqtan.supabase.co:5432/postgres?ssl=require"
engine = create_async_engine(DATABASE_URL, echo=True)
