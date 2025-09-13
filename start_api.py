#!/usr/bin/env python3
"""
Script de lancement de l'API ObesiTrack
"""

import sys
import os
import asyncio

# Ajouter le dossier backend au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Teste tous les imports nécessaires"""
    print("🔍 Test des imports...")
    
    try:
        from app.main import app
        print("✅ Import app.main réussi")
    except Exception as e:
        print(f" Erreur import app.main: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_database():
    """Teste la base de données"""
    print("\n🔍 Test de la base de données...")
    
    try:
        from app.db.session import async_session, init_db
        print("✅ Import session DB réussi")
        
        # Test d'initialisation de la DB
        asyncio.run(init_db())
        print("✅ Initialisation DB réussie")
        
    except Exception as e:
        print(f" Erreur DB: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def start_server():
    """Lance le serveur uvicorn"""
    print("\n🚀 Lancement du serveur...")
    
    try:
        import uvicorn
        from app.main import app
        
        print("✅ Serveur prêt à démarrer")
        print("🌐 API disponible sur: http://localhost:8001")
        print("📚 Documentation: http://localhost:8001/docs")
        print("🛑 Appuyez sur Ctrl+C pour arrêter")
        
        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
        
    except Exception as e:
        print(f" Erreur serveur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Démarrage de l'API ObesiTrack\n")
    
    if not test_imports():
        print("\n Échec des tests d'import. Arrêt.")
        sys.exit(1)
    
    if not test_database():
        print("\n Échec des tests de base de données. Arrêt.")
        sys.exit(1)
    
    print("\n✅ Tous les tests sont passés !")
    start_server()
