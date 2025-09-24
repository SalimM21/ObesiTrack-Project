#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à la base de données
"""

import asyncio
import sys
import os

# Ajouter le répertoire backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_connection():
    try:
        print("🔍 Test de connexion à la base de données...")
        
        from app.db.session import async_session, init_db
        from app.db.models import User, Prediction
        from app.core.security import hash_password
        from sqlalchemy import select
        
        print("✅ Imports réussis")
        
        # Initialiser la base de données
        print("🔧 Initialisation de la base de données...")
        await init_db()
        print("✅ Base de données initialisée")
        
        # Tester la connexion
        async with async_session() as session:
            print("🔗 Test de connexion...")
            result = await session.execute(select(User))
            users = result.scalars().all()
            print(f"✅ Connexion réussie! {len(users)} utilisateurs trouvés")
            
            # Afficher quelques utilisateurs
            for user in users[:5]:
                print(f"   - {user.full_name} ({user.email}) - {user.role}")
        
        print("🎉 Test terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
