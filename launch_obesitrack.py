#!/usr/bin/env python3
"""
Script de lancement complet pour ObesiTrack
Lance l'API et le frontend avec gestion des erreurs
"""

import subprocess
import time
import sys
import os
import signal
import threading
import requests
from pathlib import Path

class ObesiTrackLauncher:
    def __init__(self):
        self.api_process = None
        self.frontend_process = None
        self.running = True
        
    def check_port(self, port):
        """Vérifie si un port est libre"""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) != 0
    
    def kill_process_on_port(self, port):
        """Tue le processus utilisant un port"""
        try:
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
                        print(f"✅ Processus sur le port {port} terminé")
                        return True
        except Exception as e:
            print(f"⚠️  Erreur lors de la libération du port {port}: {e}")
        return False
    
    def start_api(self):
        """Lance l'API"""
        print("🚀 Lancement de l'API...")
        
        # Vérifier le port 8001
        if not self.check_port(8001):
            print("⚠️  Port 8001 occupé, libération...")
            self.kill_process_on_port(8001)
            time.sleep(2)
        
        try:
            self.api_process = subprocess.Popen([
                sys.executable, 'start_api.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Attendre que l'API démarre
            for i in range(10):
                time.sleep(1)
                try:
                    response = requests.get("http://localhost:8001/", timeout=2)
                    if response.status_code == 200:
                        print("✅ API démarrée avec succès sur http://localhost:8001")
                        return True
                except:
                    continue
            
            print("❌ L'API n'a pas pu démarrer")
            return False
            
        except Exception as e:
            print(f"❌ Erreur lors du lancement de l'API: {e}")
            return False
    
    def start_frontend(self):
        """Lance le frontend"""
        print("🌐 Lancement du frontend...")
        
        # Vérifier le port 3000
        if not self.check_port(3000):
            print("⚠️  Port 3000 occupé, libération...")
            self.kill_process_on_port(3000)
            time.sleep(2)
        
        try:
            self.frontend_process = subprocess.Popen([
                sys.executable, 'serve_frontend.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Attendre que le frontend démarre
            for i in range(5):
                time.sleep(1)
                try:
                    response = requests.get("http://localhost:3000/", timeout=2)
                    if response.status_code == 200:
                        print("✅ Frontend démarré avec succès sur http://localhost:3000")
                        return True
                except:
                    continue
            
            print("❌ Le frontend n'a pas pu démarrer")
            return False
            
        except Exception as e:
            print(f"❌ Erreur lors du lancement du frontend: {e}")
            return False
    
    def monitor_processes(self):
        """Surveille les processus en arrière-plan"""
        while self.running:
            time.sleep(5)
            
            # Vérifier l'API
            if self.api_process and self.api_process.poll() is not None:
                print("⚠️  L'API s'est arrêtée, redémarrage...")
                self.start_api()
            
            # Vérifier le frontend
            if self.frontend_process and self.frontend_process.poll() is not None:
                print("⚠️  Le frontend s'est arrêté, redémarrage...")
                self.start_frontend()
    
    def stop_all(self):
        """Arrête tous les processus"""
        print("\n🛑 Arrêt des services...")
        self.running = False
        
        if self.api_process:
            self.api_process.terminate()
            print("✅ API arrêtée")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend arrêté")
    
    def run(self):
        """Lance l'application complète"""
        print("🚀 Démarrage d'ObesiTrack")
        print("=" * 40)
        
        # Vérifier que les fichiers existent
        if not Path("start_api.py").exists():
            print("❌ Fichier start_api.py introuvable")
            return False
        
        if not Path("serve_frontend.py").exists():
            print("❌ Fichier serve_frontend.py introuvable")
            return False
        
        # Lancer l'API
        if not self.start_api():
            return False
        
        # Lancer le frontend
        if not self.start_frontend():
            self.stop_all()
            return False
        
        print("\n🎉 ObesiTrack est maintenant opérationnel!")
        print("\n🌐 URLs disponibles:")
        print("   - API: http://localhost:8001")
        print("   - Documentation: http://localhost:8001/docs")
        print("   - Frontend: http://localhost:3000")
        print("   - Test: http://localhost:3000/test_frontend.html")
        print("\n📊 Données de test disponibles:")
        print("   - 32 utilisateurs (22 normaux + 10 admins)")
        print("   - 30 prédictions")
        print("   - Mots de passe: password123 (users) / admin123 (admins)")
        print("\n🛑 Appuyez sur Ctrl+C pour arrêter")
        
        # Démarrer la surveillance
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            self.stop_all()
            print("\n👋 Au revoir!")
        
        return True

def main():
    launcher = ObesiTrackLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
