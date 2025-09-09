
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from .session import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(10), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    age = Column(Integer, nullable=False)
    fcvc = Column(Integer)
    caloric_intake = Column(Integer)
    active_level = Column(Integer)
    weight = Column(DECIMAL)
    height = Column(DECIMAL)
    result = Column(String(50))
    probability = Column(DECIMAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


