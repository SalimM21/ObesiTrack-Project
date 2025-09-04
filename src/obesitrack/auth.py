from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from obesitrack.models_sqlalchemy import User
from .config import settings  # pydantic settings with SECRET_KEY, ALGORITHM, EXPIRE_MINUTES
from .db import get_db_session  # Import get_db_session from your db module

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(plain, hashed): return pwd_ctx.verify(plain, hashed)
def hash_password(p): return pwd_ctx.hash(p)

from datetime import datetime, timedelta, timezone

def create_access_token(sub: str, role: str, expires_minutes: int | None = None):
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": sub, "role": role, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2), db=Depends(get_db_session)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        # load user from DB
        user = db.query(User).filter_by(username=username).first()
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privilege required")
    return user
