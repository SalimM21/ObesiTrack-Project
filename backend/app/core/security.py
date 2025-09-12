from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------- Utils Hash -----------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_ctx.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
	return pwd_ctx.hash(password)


# ----------------- JWT -----------------
def create_access_token(sub: str, role: str, expires_minutes: int | None = None) -> str:
	expire = datetime.now(timezone.utc) + timedelta(
		minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
	)
	payload = {"sub": sub, "role": role, "exp": expire}
	return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		return payload
	except JWTError:
		return None
