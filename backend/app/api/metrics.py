from fastapi import APIRouter
import json

# Pour l'exemple, on stocke les métriques dans un dictionnaire.
# Dans un projet réel, tu peux calculer les métriques via ton modèle
# ou les lire depuis un fichier / base de données.
MODEL_METRICS = {
    "accuracy": 0.87,
    "precision": 0.85,
    "recall": 0.82,
    "f1_score": 0.835
}

router = APIRouter()

@router.get("/metrics", tags=["Metrics"])
def get_model_metrics():
    """
    Endpoint pour récupérer les métriques minimales du modèle.
    """
    return {"model_metrics": MODEL_METRICS}
