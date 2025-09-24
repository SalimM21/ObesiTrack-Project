#!/usr/bin/env python3
"""
Script simple pour ajouter des données de test dans la base de données ObesiTrack
- 30 prédictions
- 20 utilisateurs
- 10 administrateurs
"""

import sqlite3
import json
import random
from datetime import datetime

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

def hash_password(password: str) -> str:
    """Hash simple pour les tests (en production, utiliser bcrypt)"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

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
        
        # Probabilité basée sur l'IMC
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

def add_test_data():
    """Ajoute les données de test à la base de données"""
    print("🚀 Ajout des données de test...")
    
    try:
        conn = sqlite3.connect('obesitrack.db')
        cursor = conn.cursor()
        
        # Vérifier les données existantes
        cursor.execute("SELECT COUNT(*) FROM users")
        existing_users = cursor.fetchone()[0]
        
        if existing_users > 0:
            print(f"⚠️  {existing_users} utilisateurs existent déjà dans la base de données.")
            response = input("Voulez-vous continuer et ajouter plus de données ? (y/N): ")
            if response.lower() != 'y':
                print("❌ Opération annulée.")
                return
        
        print("👥 Ajout des utilisateurs...")
        # Ajouter les utilisateurs
        for user_data in USERS_DATA:
            cursor.execute("""
                INSERT INTO users (full_name, email, hashed_password, role, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_data["full_name"],
                user_data["email"],
                hash_password("password123"),
                "user",
                datetime.now().isoformat()
            ))
        
        print("👨‍💼 Ajout des administrateurs...")
        # Ajouter les administrateurs
        for admin_data in ADMINS_DATA:
            cursor.execute("""
                INSERT INTO users (full_name, email, hashed_password, role, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                admin_data["full_name"],
                admin_data["email"],
                hash_password("admin123"),
                "admin",
                datetime.now().isoformat()
            ))
        
        print("✅ Utilisateurs et administrateurs ajoutés avec succès!")
        
        # Récupérer les IDs des utilisateurs pour les prédictions
        cursor.execute("SELECT id FROM users WHERE role = 'user'")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        print("🔮 Génération des prédictions...")
        predictions_data = generate_prediction_data()
        
        print("💾 Ajout des prédictions...")
        # Ajouter les prédictions
        for pred_data in predictions_data:
            # Assigner aléatoirement à un utilisateur
            user_id = random.choice(user_ids)
            
            cursor.execute("""
                INSERT INTO predictions (user_id, payload, result, probability, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id,
                pred_data["payload"],
                pred_data["result"],
                pred_data["probability"],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        print("✅ Prédictions ajoutées avec succès!")
        
        # Afficher un résumé
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'user'")
        users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admins = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM predictions")
        predictions = cursor.fetchone()[0]
        
        print("\n📊 Résumé des données ajoutées:")
        print(f"   👥 Total utilisateurs: {total_users}")
        print(f"   👤 Utilisateurs normaux: {users}")
        print(f"   👨‍💼 Administrateurs: {admins}")
        print(f"   🔮 Prédictions: {predictions}")
        print("\n🎉 Données de test ajoutées avec succès!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des données: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 Script d'ajout de données de test pour ObesiTrack")
    print("=" * 50)
    add_test_data()
