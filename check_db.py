#!/usr/bin/env python3
"""
Script pour vérifier le contenu de la base de données
"""

import sqlite3

def check_database():
    try:
        print("🔍 Vérification de la base de données...")
        
        conn = sqlite3.connect('obesitrack.db')
        cursor = conn.cursor()
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables trouvées: {[table[0] for table in tables]}")
        
        # Compter les utilisateurs
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"👥 Nombre d'utilisateurs: {user_count}")
        
        # Compter les prédictions
        cursor.execute("SELECT COUNT(*) FROM predictions")
        prediction_count = cursor.fetchone()[0]
        print(f"🔮 Nombre de prédictions: {prediction_count}")
        
        # Afficher quelques utilisateurs
        if user_count > 0:
            cursor.execute("SELECT full_name, email, role FROM users LIMIT 5")
            users = cursor.fetchall()
            print("\n👤 Premiers utilisateurs:")
            for user in users:
                print(f"   - {user[0]} ({user[1]}) - {user[2]}")
        
        # Afficher quelques prédictions
        if prediction_count > 0:
            cursor.execute("SELECT result, probability FROM predictions LIMIT 5")
            predictions = cursor.fetchall()
            print("\n🔮 Premières prédictions:")
            for pred in predictions:
                print(f"   - {pred[0]} (prob: {pred[1]})")
        
        conn.close()
        print("\n✅ Vérification terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database()
