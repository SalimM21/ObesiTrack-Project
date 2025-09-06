import random
from typing import Dict, Tuple


def predict(payload: dict) -> Tuple[str, Dict[str, float]]:
    """
    Simule une prédiction binaire avec des probabilités.
    À remplacer par un vrai modèle (pickle / joblib).
    
    Args:
        payload (dict): Les données d'entrée (ex: âge, poids, etc.)

    Returns:
        Tuple[str, Dict[str, float]]: (étiquette, probabilités)
    """
    p_positive = round(random.uniform(0, 1), 3)
    p_negative = round(1 - p_positive, 3)

    label = "Obésité probable" if p_positive >= 0.5 else "Obésité improbable"

    return label, {"positive": p_positive, "negative": p_negative}
