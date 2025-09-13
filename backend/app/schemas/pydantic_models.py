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
    # Features pour la prédiction d'obésité
    age: int
    gender: str  # Male/Female
    height: float
    weight: float
    family_history_with_overweight: str  # yes/no
    favc: str  # yes/no (frequent consumption of high caloric food)
    fcvc: int  # frequency of consumption of vegetables
    ncp: int  # number of main meals
    caec: str  # consumption of food between meals
    smoke: str  # yes/no
    ch2o: int  # consumption of water daily
    scc: str  # calories consumption monitoring
    faf: int  # physical activity frequency
    tue: int  # time using technology devices
    cal: int  # consumption of alcohol
    mtrans: str  # transportation used

class PredictionOut(BaseModel):
    result: str
    probability: Dict[str, float]
