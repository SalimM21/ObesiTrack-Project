import random
import json
from typing import Dict, Tuple
import os
from pathlib import Path

def predict(payload: dict) -> Tuple[str, Dict[str, float]]:
    """
    Prédiction d'obésité basée sur les données d'entrée.
    Utilise un modèle de machine learning si disponible, sinon simulation.
    
    Args:
        payload (dict): Les données d'entrée (âge, poids, etc.)

    Returns:
        Tuple[str, Dict[str, float]]: (étiquette, probabilités)
    """
    try:
        # Essayer de charger le modèle ML s'il existe
        model_path = Path(__file__).parent.parent.parent / "models" / "data" / "gradient_boosting_model.pkl"
        if model_path.exists():
            import joblib
            import numpy as np
            
            # Charger le modèle
            model = joblib.load(model_path)
            
            # Préparer les données pour le modèle
            # Note: Vous devrez adapter cette partie selon votre modèle
            features = [
                payload.get('age', 25),
                payload.get('height', 1.70),
                payload.get('weight', 70),
                payload.get('fcvc', 2),
                payload.get('ncp', 3),
                payload.get('ch2o', 2),
                payload.get('faf', 1),
                payload.get('tue', 1),
                payload.get('cal', 0),
            ]
            
            # Faire la prédiction
            prediction = model.predict([features])[0]
            probabilities = model.predict_proba([features])[0]
            
            # Mapper les classes (ajustez selon votre modèle)
            class_names = ['Insufficient_Weight', 'Normal_Weight', 'Overweight_Level_I', 
                          'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']
            
            if prediction < len(class_names):
                label = class_names[prediction]
            else:
                label = "Unknown"
            
            # Créer le dictionnaire de probabilités
            prob_dict = {class_names[i]: float(prob) for i, prob in enumerate(probabilities) if i < len(class_names)}
            
            return label, prob_dict
            
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {e}")
    
    # Fallback: simulation si le modèle n'est pas disponible
    p_positive = round(random.uniform(0, 1), 3)
    p_negative = round(1 - p_positive, 3)

    label = "Obésité probable" if p_positive >= 0.5 else "Obésité improbable"

    return label, {"positive": p_positive, "negative": p_negative}
