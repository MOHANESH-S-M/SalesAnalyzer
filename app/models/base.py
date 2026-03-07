from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String,Date, ForeignKey

class Base(DeclarativeBase):
    pass

class Sales(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    product_name = Column(String,nullable=False)
    quantity = Column(Integer,nullable=False,default=1)
    selling_price = Column(Integer,nullable=False)
    category = Column(String,nullable=False)
    date = Column(Date,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to users.id
    user = relationship("User", back_populates="sales")  # Relationship to user

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    sales = relationship("Sales", back_populates="user")  # Relationship to sales