
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.api.deps import get_current_user
from app.db.session import async_session
from app.db.models import User

router = APIRouter(prefix="/users", tags=["users"])

def admin_required(user):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

@router.get("/")
async def list_users(current_user=Depends(get_current_user)):
    admin_required(current_user)
    async with async_session() as session:
        q = select(User)
        r = await session.exec(q)
        return r.all()

@router.patch("/{user_id}/role")
async def change_role(user_id: int, role: str, current_user=Depends(get_current_user)):
    admin_required(current_user)
    async with async_session() as session:
        q = select(User).where(User.id == user_id)
        r = await session.exec(q)
        user = r.one_or_none()
        if not user:
            raise HTTPException(404, "Utilisateur non trouvé")
        user.role = role
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user=Depends(get_current_user)):
    admin_required(current_user)
    async with async_session() as session:
        q = select(User).where(User.id == user_id)
        r = await session.exec(q)
        user = r.one_or_none()
        if not user:
            raise HTTPException(404, "Utilisateur non trouvé")
        await session.delete(user)
        await session.commit()
        return {"ok": True}
