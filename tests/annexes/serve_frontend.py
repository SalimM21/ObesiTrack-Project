#!/usr/bin/env python3
"""
Serveur web simple pour servir les pages HTML du frontend
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Port pour le serveur frontend
PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="frontend", **kwargs)
    
    def end_headers(self):
        # Ajouter les headers CORS pour permettre les requêtes depuis le frontend
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

def start_frontend_server():
    """Démarre le serveur frontend"""
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🌐 Serveur frontend démarré sur http://localhost:{PORT}")
            print(f"📁 Dossier servi: {os.path.abspath('frontend')}")
            print(f"🧪 Page de test: http://localhost:{PORT}/test_frontend.html")
            print(f"🔗 Pages disponibles:")
            print(f"   - Connexion: http://localhost:{PORT}/index.html")
            print(f"   - Inscription: http://localhost:{PORT}/register.html")
            print(f"   - Prédiction: http://localhost:{PORT}/add_patient.html")
            print(f"   - Dashboard: http://localhost:{PORT}/dashboard.html")
            print(f"🛑 Appuyez sur Ctrl+C pour arrêter")
            
            # Ouvrir automatiquement la page de test
            webbrowser.open(f'http://localhost:{PORT}/test_frontend.html')
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté")
    except OSError as e:
        if e.errno == 10048:  # Port déjà utilisé
            print(f"❌ Erreur: Le port {PORT} est déjà utilisé")
            print(f"💡 Essayez de fermer l'autre application ou changez le port")
        else:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage du serveur frontend ObesiTrack")
    print("⚠️  Assurez-vous que l'API est démarrée sur http://localhost:8001")
    print()
    
    start_frontend_server()
