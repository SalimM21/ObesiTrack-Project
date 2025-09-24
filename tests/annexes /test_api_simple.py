#!/usr/bin/env python3
"""
Script de test simple pour l'API ObesiTrack
"""

import requests
import json

API_URL = "http://localhost:8001"

def test_api():
    print("🧪 Test de l'API ObesiTrack")
    print("=" * 50)
    
    # 1. Test de connexion API
    print("1. Test de connexion API...")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"✅ API accessible: {response.json()}")
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return
    
    # 2. Test d'inscription
    print("\n2. Test d'inscription...")
    signup_data = {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(f"{API_URL}/auth/signup", json=signup_data)
        if response.status_code == 200:
            print("✅ Inscription réussie")
        else:
            print(f"⚠️ Inscription: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erreur inscription: {e}")
    
    # 3. Test de connexion
    print("\n3. Test de connexion...")
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{API_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access_token')
            print(f"✅ Connexion réussie, token: {token[:30]}...")
        else:
            print(f"❌ Erreur connexion: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return
    
    # 4. Test de prédiction
    print("\n4. Test de prédiction...")
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
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{API_URL}/predictions/predict", json=prediction_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prédiction réussie: {result}")
        else:
            print(f"❌ Erreur prédiction: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erreur prédiction: {e}")
    
    # 5. Test d'historique
    print("\n5. Test d'historique...")
    try:
        response = requests.get(f"{API_URL}/predictions/me", headers=headers)
        if response.status_code == 200:
            history = response.json()
            print(f"✅ Historique chargé: {len(history)} prédictions")
        else:
            print(f"❌ Erreur historique: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erreur historique: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Tests terminés !")

if __name__ == "__main__":
    test_api()
