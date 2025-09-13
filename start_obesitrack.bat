@echo off
echo 🚀 Démarrage d'ObesiTrack
echo ========================

echo.
echo 📡 Lancement de l'API...
start "API ObesiTrack" cmd /k "python start_api.py"

echo.
echo ⏳ Attente du démarrage de l'API...
timeout /t 5 /nobreak > nul

echo.
echo 🌐 Lancement du Frontend...
start "Frontend ObesiTrack" cmd /k "python serve_frontend.py"

echo.
echo ⏳ Attente du démarrage du Frontend...
timeout /t 3 /nobreak > nul

echo.
echo ✅ ObesiTrack est maintenant opérationnel!
echo.
echo 🌐 URLs disponibles:
echo    - API: http://localhost:8001
echo    - Documentation: http://localhost:8001/docs
echo    - Frontend: http://localhost:3000
echo    - Test: http://localhost:3000/test_frontend.html
echo.
echo 📊 Données de test:
echo    - 32 utilisateurs (22 normaux + 10 admins)
echo    - 30 prédictions
echo    - Mots de passe: password123 (users) / admin123 (admins)
echo.
echo 🛑 Fermez les fenêtres pour arrêter les services
echo.

pause
