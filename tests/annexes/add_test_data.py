#!/usr/bin/env python3
"""
Script pour ajouter des données de test dans la base de données ObesiTrack
- 30 prédictions
- 20 utilisateurs
- 10 administrateurs
"""

import asyncio
import json
import random
import sys
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Ajouter le répertoire backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.db.session import async_session, init_db
from app.db.models import User, Prediction
from app.core.security import hash_password

# Données pour les utilisateurs
USERS_DATA = [
    {"full_name": "Alice Dupont", "email": "alice.dupont@example.com"},
    {"full_name": "Jean Martin", "email": "jean.martin@example.com"},
    {"full_name": "Sarah Bernard", "email": "sarah.bernard@example.com"},
    {"full_name": "David Laurent", "email": "david.laurent@example.com"},
    {"full_name": "Emma Richard", "email": "emma.richard@example.com"},
    {"full_name": "Lucas Petit", "email": "lucas.petit@example.com"},
    {"full_name": "Marie Fabre", "email": "marie.fabre@example.com"},
    {"full_name": "Hugo Leroy", "email": "hugo.leroy@example.com"},
    {"full_name": "Chloé Moreau", "email": "chloe.moreau@example.com"},
    {"full_name": "Antoine Garcia", "email": "antoine.garcia@example.com"},
    {"full_name": "Julie Thomas", "email": "julie.thomas@example.com"},
    {"full_name": "Louis Renaud", "email": "louis.renaud@example.com"},
    {"full_name": "Manon Leclerc", "email": "manon.leclerc@example.com"},
    {"full_name": "Paul Robert", "email": "paul.robert@example.com"},
    {"full_name": "Laura Fontaine", "email": "laura.fontaine@example.com"},
    {"full_name": "Maxime Olivier", "email": "maxime.olivier@example.com"},
    {"full_name": "Camille Chevalier", "email": "camille.chevalier@example.com"},
    {"full_name": "Thomas Lemoine", "email": "thomas.lemoine@example.com"},
    {"full_name": "Élise Blanc", "email": "elise.blanc@example.com"},
    {"full_name": "Nicolas Dupuis", "email": "nicolas.dupuis@example.com"},
]

# Données pour les administrateurs
ADMINS_DATA = [
    {"full_name": "Admin Principal", "email": "admin.principal@obesitrack.com"},
    {"full_name": "Admin Secondaire", "email": "admin.secondaire@obesitrack.com"},
    {"full_name": "Admin Technique", "email": "admin.technique@obesitrack.com"},
    {"full_name": "Admin Médical", "email": "admin.medical@obesitrack.com"},
    {"full_name": "Admin Support", "email": "admin.support@obesitrack.com"},
    {"full_name": "Admin Data", "email": "admin.data@obesitrack.com"},
    {"full_name": "Admin Analytics", "email": "admin.analytics@obesitrack.com"},
    {"full_name": "Admin Quality", "email": "admin.quality@obesitrack.com"},
    {"full_name": "Admin Operations", "email": "admin.operations@obesitrack.com"},
    {"full_name": "Admin Superviseur", "email": "admin.superviseur@obesitrack.com"},
]

def generate_prediction_data():
    """Génère des données de prédiction réalistes"""
    ages = list(range(18, 80))
    heights = [round(random.uniform(1.50, 2.00), 2) for _ in range(100)]
    weights = [round(random.uniform(45, 150), 1) for _ in range(100)]
    
    family_history_options = ["yes", "no"]
    favc_options = ["yes", "no"]
    fcvc_values = [round(random.uniform(1.0, 3.0), 1) for _ in range(100)]
    ncp_values = list(range(1, 9))
    caec_options = ["no", "sometimes", "frequently", "always"]
    smoke_options = ["yes", "no"]
    ch2o_values = [round(random.uniform(0.5, 10.0), 1) for _ in range(100)]
    scc_options = ["yes", "no"]
    faf_values = [round(random.uniform(0.0, 7.0), 1) for _ in range(100)]
    tue_values = [round(random.uniform(0.0, 24.0), 1) for _ in range(100)]
    calc_options = ["no", "sometimes", "frequently", "always"]
    mtrans_options = ["Public_Transportation", "Automobile", "Walking", "Bike", "Motorbike"]
    
    # Résultats possibles avec probabilités
    results = ["Normal_Weight", "Overweight_Level_I", "Overweight_Level_II", "Obesity_Type_I", "Obesity_Type_II", "Obesity_Type_III"]
    
    predictions = []
    for i in range(30):
        # Calculer l'IMC pour déterminer un résultat plus réaliste
        age = random.choice(ages)
        height = random.choice(heights)
        weight = random.choice(weights)
        bmi = weight / (height ** 2)
        
        # Déterminer le résultat basé sur l'IMC
        if bmi < 18.5:
            result = "Insufficient_Weight"
        elif bmi < 25:
            result = "Normal_Weight"
        elif bmi < 30:
            result = "Overweight_Level_I"
        elif bmi < 35:
            result = "Obesity_Type_I"
        elif bmi < 40:
            result = "Obesity_Type_II"
        else:
            result = "Obesity_Type_III"
        
        # Probabilité basée sur l'IMC (plus l'IMC s'éloigne de la normale, plus la probabilité est élevée)
        if result == "Normal_Weight":
            probability = round(random.uniform(0.7, 0.95), 3)
        else:
            probability = round(random.uniform(0.8, 0.98), 3)
        
        payload = {
            "age": age,
            "height": height,
            "weight": weight,
            "family_history_with_overweight": random.choice(family_history_options),
            "FAVC": random.choice(favc_options),
            "FCVC": random.choice(fcvc_values),
            "NCP": random.choice(ncp_values),
            "CAEC": random.choice(caec_options),
            "SMOKE": random.choice(smoke_options),
            "CH2O": random.choice(ch2o_values),
            "SCC": random.choice(scc_options),
            "FAF": random.choice(faf_values),
            "TUE": random.choice(tue_values),
            "CALC": random.choice(calc_options),
            "MTRANS": random.choice(mtrans_options)
        }
        
        predictions.append({
            "payload": json.dumps(payload),
            "result": result,
            "probability": probability
        })
    
    return predictions

async def add_test_data():
    """Ajoute les données de test à la base de données"""
    print("🚀 Initialisation de la base de données...")
    await init_db()
    
    async with async_session() as session:
        try:
            # Vérifier si des données existent déjà
            result = await session.execute(select(User))
            existing_users = result.scalars().all()
            
            if len(existing_users) > 0:
                print(f"⚠️  {len(existing_users)} utilisateurs existent déjà dans la base de données.")
                response = input("Voulez-vous continuer et ajouter plus de données ? (y/N): ")
                if response.lower() != 'y':
                    print("❌ Opération annulée.")
                    return
            
            print("👥 Ajout des utilisateurs...")
            # Ajouter les utilisateurs
            for user_data in USERS_DATA:
                user = User(
                    full_name=user_data["full_name"],
                    email=user_data["email"],
                    hashed_password=hash_password("password123"),
                    role="user"
                )
                session.add(user)
            
            print("👨‍💼 Ajout des administrateurs...")
            # Ajouter les administrateurs
            for admin_data in ADMINS_DATA:
                admin = User(
                    full_name=admin_data["full_name"],
                    email=admin_data["email"],
                    hashed_password=hash_password("admin123"),
                    role="admin"
                )
                session.add(admin)
            
            await session.commit()
            print("✅ Utilisateurs et administrateurs ajoutés avec succès!")
            
            # Récupérer les IDs des utilisateurs pour les prédictions
            result = await session.execute(select(User.id).where(User.role == "user"))
            user_ids = [row[0] for row in result.fetchall()]
            
            print("🔮 Génération des prédictions...")
            predictions_data = generate_prediction_data()
            
            print("💾 Ajout des prédictions...")
            # Ajouter les prédictions
            for i, pred_data in enumerate(predictions_data):
                # Assigner aléatoirement à un utilisateur
                user_id = random.choice(user_ids)
                
                prediction = Prediction(
                    user_id=user_id,
                    payload=pred_data["payload"],
                    result=pred_data["result"],
                    probability=pred_data["probability"]
                )
                session.add(prediction)
            
            await session.commit()
            print("✅ Prédictions ajoutées avec succès!")
            
            # Afficher un résumé
            result = await session.execute(select(User))
            all_users = result.scalars().all()
            
            result = await session.execute(select(User).where(User.role == "user"))
            users = result.scalars().all()
            
            result = await session.execute(select(User).where(User.role == "admin"))
            admins = result.scalars().all()
            
            result = await session.execute(select(Prediction))
            predictions = result.scalars().all()
            
            print("\n📊 Résumé des données ajoutées:")
            print(f"   👥 Total utilisateurs: {len(all_users)}")
            print(f"   👤 Utilisateurs normaux: {len(users)}")
            print(f"   👨‍💼 Administrateurs: {len(admins)}")
            print(f"   🔮 Prédictions: {len(predictions)}")
            print("\n🎉 Données de test ajoutées avec succès!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Erreur lors de l'ajout des données: {e}")
            raise

if __name__ == "__main__":
    print("🔧 Script d'ajout de données de test pour ObesiTrack")
    print("=" * 50)
    asyncio.run(add_test_data())
