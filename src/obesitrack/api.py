from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import pandas as pd
from .schemas import PredictRequest, PredictResponse
from .security import get_current_user, token_endpoint
from .model import registry
from .logging_conf import setup_logging


setup_logging()

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute", "1000/hour"]) # ajustez selon besoin

middleware = [
Middleware(GZipMiddleware, minimum_size=500),
Middleware(SessionMiddleware, secret_key="dummy"),
]

app = FastAPI(title="ObesiTrack API", version="1.0.0", middleware=middleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.state

@app.post("/predict", response_model=PredictOut)
async def predict(payload: PredictIn, user=Depends(get_current_user), db=Depends(get_db_session)):
    df = pd.DataFrame([payload.model_dump()])
    bundle = registry.load()
    probs = bundle.predict_proba(df)[0]
    classes = list(bundle.classifier.classes_)
    prob_map = {c: float(p) for c, p in zip(classes, probs)}
    label = classes[int(probs.argmax())]
    # persist
    pred = Prediction(
        user_id=user.id,
        input_json=payload.model_dump(),
        predicted_label=label,
        probabilities=prob_map,
        model_name=str(bundle.classifier.__class__.__name__),
        model_version=getattr(bundle.classifier, "version", "v1")
    )
    db.add(pred); db.commit()
    return PredictOut(label=label, probabilities=prob_map, model_name=pred.model_name, model_version=pred.model_version)
