#!/usr/bin/env python3
"""
Test simple du token JWT
"""

import requests
import json
from jose import jwt

API_URL = "http://localhost:8001"

# 1. Se connecter pour obtenir un token
print("1. Connexion...")
login_data = {"email": "test@example.com", "password": "test123"}
response = requests.post(f"{API_URL}/auth/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    token_data = response.json()
    token = token_data.get('access_token')
    print(f"Token: {token[:50]}...")
    
    # 2. Décoder le token pour voir son contenu
    print("\n2. Décodage du token...")
    try:
        # Décoder sans vérification pour voir le contenu
        decoded = jwt.get_unverified_claims(token)
        print(f"Contenu du token: {json.dumps(decoded, indent=2)}")
    except Exception as e:
        print(f"Erreur décodage: {e}")
    
    # 3. Tester une requête avec le token
    print("\n3. Test de requête avec token...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test simple avec l'endpoint des métriques (pas d'auth requise)
    response = requests.get(f"{API_URL}/metrics", headers=headers)
    print(f"Métriques: {response.status_code} - {response.text}")
    
    # Test avec prédiction (auth requise)
    prediction_data = {
        "age": 25,
        "gender": "Male", 
        "height": 1.75,
        "weight": 70,
        "family_history_with_overweight": "no",
        "favc": "no",
        "fcvc": 2.5,
        "ncp": 3,
        "caec": "sometimes",
        "smoke": "no",
        "ch2o": 2.5,
        "scc": "no",
        "faf": 1.5,
        "tue": 2.5,
        "cal": 0,
        "mtrans": "Public_Transportation"
    }
    
    response = requests.post(f"{API_URL}/predictions/predict", json=prediction_data, headers=headers)
    print(f"Prédiction: {response.status_code} - {response.text}")
