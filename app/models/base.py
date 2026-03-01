from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String,Date

class Base(DeclarativeBase):
    pass

class Sales(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    product_name = Column(String,nullable=False)
    quantity = Column(Integer)
    selling_price = Column(Integer,nullable=False)
    category = Column(String,nullable=False)
    date = Column(Date,nullable=False)