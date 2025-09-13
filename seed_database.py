#!/usr/bin/env python3
"""
Script pour ajouter des données de test dans la base de données ObesiTrack
- 20 utilisateurs normaux
- 10 administrateurs
- 30 prédictions
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from faker import Faker
import sys
import os

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.db.session import async_session, engine
from backend.app.db.models import User, Prediction, Base
from backend.app.core.security import hash_password

# Initialiser Faker pour générer des données aléatoires
fake = Faker('fr_FR')

# Créer les tables si elles n'existent pas
async def create_tables():
    """Créer les tables de la base de données"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables créées/mises à jour")

async def create_users():
    """Créer 20 utilisateurs normaux et 10 administrateurs"""
    users = []
    
    # 20 utilisateurs normaux
    for i in range(20):
        user = User(
            full_name=fake.name(),
            email=fake.email(),
            hashed_password=hash_password("password123"),
            role="user",
            created_at=fake.date_time_between(start_date='-1y', end_date='now')
        )
        users.append(user)
    
    # 10 administrateurs
    for i in range(10):
        user = User(
            full_name=fake.name(),
            email=fake.email(),
            hashed_password=hash_password("admin123"),
            role="admin",
            created_at=fake.date_time_between(start_date='-1y', end_date='now')
        )
        users.append(user)
    
    # Sauvegarder en base
    async with async_session() as session:
        for user in users:
            session.add(user)
        await session.commit()
        print(f"✅ {len(users)} utilisateurs créés (20 users + 10 admins)")
    
    return users

async def create_predictions(users):
    """Créer 30 prédictions pour les utilisateurs"""
    predictions = []
    
    # Données de test pour les prédictions
    genders = ["Male", "Female"]
    family_history_options = ["yes", "no"]
    favc_options = ["yes", "no"]
    caec_options = ["sometimes", "no", "frequently", "always"]
    smoke_options = ["yes", "no"]
    scc_options = ["yes", "no"]
    mtrans_options = ["Public_Transportation", "Automobile", "Walking", "Bike", "Motorbike"]
    
    # Résultats possibles pour les prédictions
    prediction_results = [
        "Insufficient_Weight",
        "Normal_Weight", 
        "Overweight_Level_I",
        "Overweight_Level_II",
        "Obesity_Type_I",
        "Obesity_Type_II",
        "Obesity_Type_III"
    ]
    
    for i in range(30):
        # Choisir un utilisateur aléatoire
        user = random.choice(users)
        
        # Générer des données de prédiction aléatoires
        prediction_data = {
            "age": random.randint(15, 80),
            "gender": random.choice(genders),
            "height": round(random.uniform(1.50, 2.00), 2),
            "weight": round(random.uniform(45, 150), 1),
            "family_history_with_overweight": random.choice(family_history_options),
            "favc": random.choice(favc_options),
            "fcvc": round(random.uniform(1.0, 3.0), 1),
            "ncp": random.randint(1, 8),
            "caec": random.choice(caec_options),
            "smoke": random.choice(smoke_options),
            "ch2o": round(random.uniform(0.0, 10.0), 1),
            "scc": random.choice(scc_options),
            "faf": round(random.uniform(0.0, 7.0), 1),
            "tue": round(random.uniform(0.0, 24.0), 1),
            "cal": random.randint(0, 3),
            "mtrans": random.choice(mtrans_options)
        }
        
        # Générer un résultat et une probabilité aléatoires
        result = random.choice(prediction_results)
        probability = round(random.uniform(0.1, 0.99), 3)
        
        prediction = Prediction(
            user_id=user.id,
            payload=json.dumps(prediction_data),
            result=result,
            probability=probability,
            created_at=fake.date_time_between(start_date='-6m', end_date='now')
        )
        predictions.append(prediction)
    
    # Sauvegarder en base
    async with async_session() as session:
        for prediction in predictions:
            session.add(prediction)
        await session.commit()
        print(f"✅ {len(predictions)} prédictions créées")
    
    return predictions

async def main():
    """Fonction principale pour peupler la base de données"""
    print("🌱 Début du peuplement de la base de données ObesiTrack")
    print("=" * 60)
    
    try:
        # 1. Créer les tables
        await create_tables()
        
        # 2. Créer les utilisateurs
        users = await create_users()
        
        # 3. Créer les prédictions
        predictions = await create_predictions(users)
        
        print("=" * 60)
        print("🎉 Peuplement terminé avec succès !")
        print(f"📊 Résumé :")
        print(f"   - {len([u for u in users if u.role == 'user'])} utilisateurs normaux")
        print(f"   - {len([u for u in users if u.role == 'admin'])} administrateurs")
        print(f"   - {len(predictions)} prédictions")
        print("\n🔑 Comptes de test :")
        print("   - Utilisateurs : email aléatoire, mot de passe 'password123'")
        print("   - Admins : email aléatoire, mot de passe 'admin123'")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
