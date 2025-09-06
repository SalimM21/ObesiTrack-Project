import random
from typing import Tuple, Dict, Any

def predict(payload: dict) -> Tuple[str, Dict[str, float]]:
    # Mock: remplace par modèle sklearn chargé via pickle ou joblib
    p_positive = round(random.uniform(0, 1), 3)
    p_negative = round(1 - p_positive, 3)
    label = "Diabète probable" if p_positive >= 0.5 else "Diabète improbable"
    return label, {"positive": p_positive, "negative": p_negative}
