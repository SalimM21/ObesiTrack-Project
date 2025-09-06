from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    user_id: Optional[int] = None
    role: Optional[str] = None

class PredictionIn(BaseModel):
    # add your real features: age, glucose, bmi, etc.
    age: int
    glucose: float
    bmi: float
    bloodpressure: float
    pedigree: float
    sex: Optional[str] = None

class PredictionOut(BaseModel):
    result: str
    probability: Dict[str, float]
