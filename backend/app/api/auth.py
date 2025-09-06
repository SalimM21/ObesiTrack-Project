from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from app.schemas.pydantic_models import UserCreate, Token
from app.db.session import async_session
from app.db.models import User
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(payload: UserCreate):
    async with async_session() as session:
        q = select(User).where(User.email == payload.email)
        r = await session.exec(q)
        if r.first():
            raise HTTPException(status_code=400, detail="Email déjà enregistré")
        user = User(email=payload.email, hashed_password=hash_password(payload.password), full_name=payload.full_name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        token = create_access_token(subject=user.email, extra={"user_id": user.id, "role": user.role})
        return {"access_token": token}

@router.post("/login", response_model=Token)
async def login(payload: UserCreate):
    async with async_session() as session:
        q = select(User).where(User.email == payload.email)
        r = await session.exec(q)
        user = r.one_or_none()
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Identifiants incorrects")
        token = create_access_token(subject=user.email, extra={"user_id": user.id, "role": user.role})
        return {"access_token": token}
