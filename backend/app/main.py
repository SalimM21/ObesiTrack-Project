from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn import metrics

# Import des routes
from app.api import auth, users, predictions
from backend.app.services import predictor
from obesitrack.db.session import init_db

# Définir les métadonnées pour la doc Swagger
tags_metadata = [
    {
        "name": "Auth",
        "description": "Endpoints pour l'authentification et la gestion des tokens JWT.",
    },
    {
        "name": "Users",
        "description": "Gestion des utilisateurs (listes, rôles, suppression). Accessible uniquement par l'admin.",
    },
    {
        "name": "Predictions",
        "description": "Prédiction de l’obésité et consultation de l’historique des prédictions personnelles.",
    },
]

# Créer l'application FastAPI
app = FastAPI(
    title="Obesity Prediction API",
    description="API REST pour gérer l'authentification, les utilisateurs et la prédiction de l'obésité.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

# Configurer CORS (frontend peut appeler l’API sans blocage)
origins = [
    "http://localhost:5500",  # si tu ouvres le frontend avec live server
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # tu peux mettre ["*"] en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(predictor.router, prefix="/predictions", tags=["Predictions"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])


# Endpoint de test (healthcheck)
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenue sur l'API de Prédiction de l'Obésité 🚀"}


