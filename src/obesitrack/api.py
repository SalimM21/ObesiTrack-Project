import json
import os
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

from obesitrack.drift import build_drift_report
from obesitrack.models_sqlalchemy import Prediction
from obesitrack.observability import init_tracing
from .schemas import PredictIn, PredictOut, PredictRequest, PredictResponse
from .security import get_current_user, token_endpoint
from .model import registry
from .logging_conf import setup_logging

from fastapi import APIRouter, Depends, HTTPException
from .auth import get_current_user, require_admin
import pandas as pd
from .explain import ShapExplainerWrapper, _hash_payload


setup_logging()

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute", "1000/hour"]) # ajustez selon besoin

middleware = [
Middleware(GZipMiddleware, minimum_size=500),
Middleware(SessionMiddleware, secret_key="dummy"),
]

app = FastAPI(title="ObesiTrack API", version="1.0.0", middleware=middleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.state

init_tracing(app, service_name="obesitrack", otlp_endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"))

router = APIRouter()
# assume global explainer is loaded at app startup
GLOBAL_EXPLAINER: ShapExplainerWrapper = None

# ----------------------------------------
templates = Jinja2Templates(directory="src/obesitrack/templates")

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# -------------------------------


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

@router.post("/explain/shap")
async def explain_shap(payload: dict, user = Depends(get_current_user)):
    # limit input size
    if isinstance(payload, list):
        if len(payload) > 4:
            raise HTTPException(status_code=400, detail="Max 4 instances allowed")
    else:
        payload = [payload]
    key = _hash_payload(json.dumps(payload, sort_keys=True))
    # caching can be implemented with redis for persistence
    df = pd.DataFrame(payload)
    try:
        res = GLOBAL_EXPLAINER.explain(df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return res

@router.get("/drift/report")
def drift_report(user = Depends(require_admin)):
    # load baseline from file / bucket
    baseline = pd.read_csv("data/baseline.csv")
    # load last N predictions from DB (convert input_json -> dataframe)
    preds = load_recent_predictions_from_db(limit=1000)  # implement helper
    current_df = pd.DataFrame([p["input_json"] for p in preds])
    report = build_drift_report(baseline, current_df)
    return report.as_dict()  # or return minimal summary

# Planifier un job (cron) pour générer des rapports réguliers et alerter si drift détecté.
# Pour visualiser, Evidently fournit HTML export (report.save_html("drift_report.html")) — tu peux servir ce HTML via un endpoint sécurisé.
# report.save_html("drift_report.html")  # Removed because 'report' is not defined in this scope
