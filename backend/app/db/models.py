
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Float
from sqlalchemy.sql import func
from .session import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=True)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(10), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    payload = Column(String(1000))  # JSON string des données d'entrée
    result = Column(String(50))
    probability = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


