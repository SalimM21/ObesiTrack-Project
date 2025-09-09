from datetime import timedelta
import datetime
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Optional
from app.core.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_access_token(subject: str, extra: dict = {}, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": subject}
    to_encode.update(extra)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import settings
from .schemas import Token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Démo: un seul utilisateur admin depuis variables d'env
USERS = {
settings.ADMIN_USERNAME: settings.ADMIN_PASSWORD_HASH
}


def verify_password(plain_password: str, password_hash: str) -> bool:
	return pwd_context.verify(plain_password, password_hash)


def authenticate_user(username: str, password: str) -> bool:
	hash_ = USERS.get(username)
	return bool(hash_ and verify_password(password, hash_))


def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		username: str | None = payload.get("sub")
		if username is None:
			raise credentials_exception
		return username
	except JWTError:
		raise credentials_exception


def token_endpoint(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
	if not authenticate_user(form_data.username, form_data.password):
		raise HTTPException(status_code=400, detail="Incorrect username or password")
	token = create_access_token({"sub": form_data.username})
	return Token(access_token=token)
