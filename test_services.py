#!/usr/bin/env python3
"""
Script pour tester que les services API et frontend sont bien démarrés
"""

import requests
import time
import webbrowser

def test_api():
    """Teste si l'API est accessible"""
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ API accessible sur http://localhost:8001")
            print(f"   Réponse: {response.json()}")
            return True
        else:
            print(f"❌ API répond avec le code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API non accessible: {e}")
        return False

def test_frontend():
    """Teste si le frontend est accessible"""
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible sur http://localhost:3000")
            return True
        else:
            print(f"❌ Frontend répond avec le code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend non accessible: {e}")
        return False

def test_api_endpoints():
    """Teste quelques endpoints de l'API"""
    endpoints = [
        ("/", "Root"),
        ("/docs", "Documentation Swagger"),
        ("/auth/login", "Login"),
        ("/users/", "Users"),
        ("/predictions/", "Predictions")
    ]
    
    print("\n🔍 Test des endpoints API:")
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://localhost:8001{endpoint}", timeout=3)
            if response.status_code in [200, 404, 422]:  # 404/422 sont normaux pour certains endpoints
                print(f"   ✅ {name}: {response.status_code}")
            else:
                print(f"   ⚠️  {name}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {name}: {e}")

def main():
    print("🚀 Test des services ObesiTrack")
    print("=" * 40)
    
    # Attendre un peu que les services démarrent
    print("⏳ Attente du démarrage des services...")
    time.sleep(3)
    
    # Tester l'API
    api_ok = test_api()
    
    # Tester le frontend
    frontend_ok = test_frontend()
    
    if api_ok:
        test_api_endpoints()
    
    print("\n📊 Résumé:")
    print(f"   API (port 8001): {'✅ OK' if api_ok else '❌ KO'}")
    print(f"   Frontend (port 3000): {'✅ OK' if frontend_ok else '❌ KO'}")
    
    if api_ok and frontend_ok:
        print("\n🎉 Tous les services sont opérationnels!")
        print("\n🌐 URLs disponibles:")
        print("   - API: http://localhost:8001")
        print("   - Documentation: http://localhost:8001/docs")
        print("   - Frontend: http://localhost:3000")
        print("   - Test Frontend: http://localhost:3000/test_frontend.html")
        
        # Ouvrir automatiquement le frontend
        try:
            webbrowser.open("http://localhost:3000/test_frontend.html")
            print("\n🔗 Page de test ouverte dans le navigateur")
        except:
            print("\n💡 Ouvrez manuellement: http://localhost:3000/test_frontend.html")
    else:
        print("\n❌ Certains services ne sont pas accessibles")
        print("💡 Vérifiez que les scripts start_api.py et serve_frontend.py sont en cours d'exécution")

if __name__ == "__main__":
    main()
