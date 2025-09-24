# Contributing to ObesiTrack

Merci de votre intérêt pour contribuer à **ObesiTrack** ! 🎉  
Ce projet repose sur la collaboration ouverte et toutes les contributions sont les bienvenues : corrections de bugs, nouvelles fonctionnalités, documentation, tests, etc.

---

## 1️⃣ Signaler un bug

Si vous trouvez un bug, merci de créer une issue avec les informations suivantes :

- **Description claire** du problème  
- **Étapes pour reproduire** le bug  
- **Comportement attendu**  
- Captures d’écran ou logs si possible  
- Version de l’application (`commit SHA`, tag Docker, etc.)

👉 Avant de soumettre un bug, vérifiez qu’il n’a pas déjà été signalé dans les issues existantes.

---

## 2️⃣ Proposer une fonctionnalité

Pour suggérer une nouvelle fonctionnalité :  

1. Consultez la liste des issues ouvertes pour vérifier qu’elle n’existe pas déjà.  
2. Créez une **Feature Request** en précisant :  
   - Une **description détaillée** de la fonctionnalité  
   - Les **cas d’usage concrets**  
   - Les **bénéfices pour les utilisateurs** (médecins, chercheurs, institutions de santé, etc.)  

---

## 3️⃣ Contribuer au code

1. **Forkez** ce dépôt.  
2. **Clonez** votre fork :  
   ```bash
   git clone https://github.com/<votre-username>/ObesiTrack.git
   cd ObesiTrack
   ```
3. Créez une branche pour votre contribution :  
   ```bash
   git checkout -b feature/ma-nouvelle-fonctionnalite
   ```
4. Installez les dépendances :  
   ```bash
   pip install -r requirements.txt
   ```
   Ou via Docker Compose :  
   ```bash
   docker compose up --build
   ```
5. Vérifiez que les tests passent :  
   ```bash
   pytest
   ```
6. Commitez vos changements avec un message explicite :  
   ```bash
   git commit -m "feat: ajout endpoint d'explicabilité SHAP"
   ```
7. Poussez vos modifications :  
   ```bash
   git push origin feature/ma-nouvelle-fonctionnalite
   ```
8. Ouvrez une **Pull Request** vers la branche principale du dépôt.

---

## 4️⃣ Bonnes pratiques de code

- Respecter les conventions **PEP8** et exécuter `flake8`.  
- Fournir des **tests unitaires/CI** pour chaque nouvelle fonctionnalité.  
- Documenter vos changements (README, docstrings, Swagger si endpoints API).  
- Vérifier la compatibilité avec Docker/Helm et la CI/CD.  

---

## 5️⃣ Documentation & Tests

- API documentée via **Swagger** : `/docs`  
- Tests exécutables avec `pytest`  
- Monitoring & Observabilité : **Prometheus + Grafana**  
- Explicabilité & Drift : **SHAP + Evidently**  

---

## 6️⃣ Code de conduite

Nous nous engageons à maintenir un environnement inclusif et respectueux.  
Merci de lire et de respecter le [Code de conduite](CODE_OF_CONDUCT.md).  

---

💡 Toute contribution, qu’il s’agisse de documentation, de correction mineure ou de nouvelle fonctionnalité majeure, est précieuse.  
Merci d’aider à faire d’**ObesiTrack** une solution robuste et utile pour la recherche et la santé publique. 🚀
