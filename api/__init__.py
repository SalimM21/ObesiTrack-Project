from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from src.obesitrack.explainability import GLOBAL_EXPLAINER
from src.obesitrack.drift import get_drift_report

app = FastAPI(title="ObesiTrack API (test shim)")
router = APIRouter()

JWT_SECRET = "testsecret"
JWT_ALG = "HS256"

@app.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = jwt.encode({"sub": form_data.username}, JWT_SECRET, algorithm=JWT_ALG)
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        username = payload.get("sub")
        if not username:
            raise ValueError("missing sub")
        return username
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/predict")
async def predict(payload: dict, user=Depends(get_current_user)):
    probs = {"Normal_Weight": 0.7, "Overweight": 0.2, "Obesity": 0.1}
    label = max(probs, key=probs.get)
    return {"label": label, "probabilities": probs, "model_name": "FakeModel", "model_version": "v1"}

@router.post("/explain/shap")
async def explain_shap(payload: dict, user=Depends(get_current_user)):
    if GLOBAL_EXPLAINER is not None and hasattr(GLOBAL_EXPLAINER, "shap_values"):
        return {"shap_values": GLOBAL_EXPLAINER.shap_values([payload])}
    return {"shap_values": [[0.0]]}

@router.get("/drift/report")
async def drift_report(user=Depends(get_current_user)):
    return get_drift_report()

app.include_router(router)


