from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.core.security import decode_access_token
from app.db.session import async_session
from app.db.models import User

# OAuth2 Password flow, lié à ton endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Vérifie le JWT et renvoie l'utilisateur correspondant depuis la DB.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalide")

    async with async_session() as session:
        q = select(User).where(User.email == payload.get("sub"))
        result = await session.execute(q)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="Utilisateur introuvable")

        return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    """
    Vérifie que l'utilisateur est admin.
    """
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privilege required")
    return user
