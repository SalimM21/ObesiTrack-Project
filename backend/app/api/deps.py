from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.db.session import async_session
from sqlmodel import select
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalide")
    # Optionnel: récupérer user complet en DB
    async with async_session() as session:
        q = select(User).where(User.id == payload.get("user_id"))
        r = await session.exec(q)
        user = r.one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="Utilisateur introuvable")
        return user
