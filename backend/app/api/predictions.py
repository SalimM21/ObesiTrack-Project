from fastapi import APIRouter, Depends
from app.schemas.pydantic_models import PredictionIn, PredictionOut
from app.api.deps import get_current_user
from app.services.predictor import predict
from app.db.session import async_session
from app.db.models import Prediction
from sqlmodel import select

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/predict", response_model=PredictionOut)
async def make_prediction(payload: PredictionIn, current_user=Depends(get_current_user)):
    label, proba = predict(payload.dict())
    pred = Prediction(user_id=current_user.id, payload=payload.dict(), result=label, probability=proba)
    async with async_session() as session:
        session.add(pred)
        await session.commit()
        await session.refresh(pred)
    return {"result": label, "probability": proba}

@router.get("/me")
async def my_history(current_user=Depends(get_current_user)):
    async with async_session() as session:
        q = select(Prediction).where(Prediction.user_id == current_user.id).order_by(Prediction.created_at.desc())
        r = await session.exec(q)
        return r.all()


