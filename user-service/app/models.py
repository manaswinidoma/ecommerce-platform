# It represents how data looks in the database. It maps to the PostgreSQL table.
from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True ,index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    user_role = Column(String(100), default='customer')
    created_at = Column (TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    last_login = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
