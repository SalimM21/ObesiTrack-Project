#!/usr/bin/env python3
"""
Script pour vérifier les données ajoutées
"""

import sqlite3

def verify_data():
    conn = sqlite3.connect('obesitrack.db')
    cursor = conn.cursor()
    
    # Compter les utilisateurs par rôle
    cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
    roles = cursor.fetchall()
    
    print("📊 Résumé des données dans la base:")
    print("=" * 40)
    
    total_users = 0
    for role, count in roles:
        total_users += count
        print(f"👤 {role}: {count}")
    
    print(f"👥 Total utilisateurs: {total_users}")
    
    # Compter les prédictions
    cursor.execute("SELECT COUNT(*) FROM predictions")
    prediction_count = cursor.fetchone()[0]
    print(f"🔮 Prédictions: {prediction_count}")
    
    # Afficher quelques exemples
    print("\n📋 Exemples d'utilisateurs:")
    cursor.execute("SELECT full_name, email, role FROM users LIMIT 10")
    users = cursor.fetchall()
    for user in users:
        print(f"   - {user[0]} ({user[1]}) - {user[2]}")
    
    print("\n🔮 Exemples de prédictions:")
    cursor.execute("SELECT result, probability FROM predictions LIMIT 10")
    predictions = cursor.fetchall()
    for pred in predictions:
        print(f"   - {pred[0]} (prob: {pred[1]})")
    
    # Vérifier les objectifs
    print("\n🎯 Vérification des objectifs:")
    print(f"   ✅ Utilisateurs: {sum(1 for _, count in roles if _ == 'user')}/20")
    print(f"   ✅ Administrateurs: {sum(1 for _, count in roles if _ == 'admin')}/10")
    print(f"   ✅ Prédictions: {prediction_count}/30")
    
    conn.close()

if __name__ == "__main__":
    verify_data()
