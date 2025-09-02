# ObesiTrack : API Sécurisée de Prédiction de l’Obésité avec FastAPI et Docker

**ObesiTrack** est une solution complète qui associe intelligence artificielle, sécurité des données et portabilité pour répondre aux besoins croissants des institutions de santé et des chercheurs dans la lutte contre l’obésité.  

L’application repose sur un modèle de Machine Learning multiclasses capable de prédire différents niveaux d’obésité à partir de variables socio-démographiques et comportementales (âge, habitudes alimentaires, activité physique, etc.).  

Elle expose ses fonctionnalités via une API REST moderne développée avec **FastAPI**, enrichie d’une authentification sécurisée **JWT** garantissant la confidentialité des utilisateurs, et d’une base **PostgreSQL** pour gérer comptes et historiques de prédictions.  

---

## 📦 Contenu du dépôt
- `src/obesitrack/` : code FastAPI (API, auth, models, DB, monitoring, explainability).  
- `models/` : artefacts ML (`preprocessor.joblib`, `classifier.joblib`).  
- `docker-compose.yml` : environnement de dev (API + Postgres + Grafana + Prometheus + otel-collector).  
- `Dockerfile` : image API.  
- `helm/obesitrack/` : Helm chart minimal.  
- `.github/workflows/ci.yml` : pipeline CI/CD (lint + tests + build & push Docker image).  
- `requirements.txt` : dépendances Python.  
- `README.md` : ce document.  

---

##  Prérequis
- Python 3.10+  
- Docker & Docker Compose  
- Helm 3  
- Compte Docker Hub et secrets CI configurés  
- (Optionnel) Redis pour rate-limiting distribué  

---

## ⚡ Installation & exécution locale (dev)
1. Cloner le repo :  
```bash
git clone <repo> obesitrack && cd obesitrack
```

2. Construire l’environnement et lancer via Docker Compose :  
```bash
docker compose up --build
```

- API : http://localhost:8000  
- Docs Swagger : http://localhost:8000/docs  
- Grafana : http://localhost:3000 (admin/admin)  

3. (Optionnel) Entraîner et sérialiser le modèle :  
```bash
python train.py --dataset data/obesity_levels.csv --model-dir models
```

---

## 🌐 Endpoints principaux
- `POST /auth/register` — créer un compte  
- `POST /auth/token` — login (OAuth2) → JWT  
- `GET /auth/me` — profil courant  
- `POST /predict` — prédiction (auth requise) — sauvegarde dans DB  
- `GET /predictions` — historique personnel  
- `GET /metrics` — métriques Prometheus  
- `GET /health` — health check  
- `POST /explain/shap` — explication SHAP  
- `GET /drift/report` — suivi drift (Evidently report)  

---

##  Observabilité & Monitoring
- **Tracing** : OpenTelemetry (OTLP exporter).  
- **Metrics** : exposition Prometheus sur `/metrics`.  
- **Dashboard** : Grafana (importer `docs/grafana-dashboard.json`).  

---

## ⚙️ CI/CD (GitHub Actions)
- Lint (flake8).  
- Tests (pytest).  
- Build & Push image Docker sur Docker Hub.  
- Export automatique du dashboard Grafana JSON.  

---

##  Déploiement Kubernetes
Helm chart minimal inclus :  
```bash
helm install obesitrack helm/obesitrack --namespace obesitrack --create-namespace
```

---

## 🧩 Explicabilité & Drift
- Endpoint SHAP : valeurs d’importance des features.  
- Evidently : génération de rapport JSON de dérive des données.  

---

## 🔒 Conseils de production
- Gérer secrets avec Vault/Azure KeyVault/GCP Secret Manager.  
- Ajouter HTTPS + Ingress (Traefik / Nginx).  
- Configurer backups Postgres.  
- Intégrer scanner sécurité (SAST/DAST).  

---

##  Références
- [FastAPI](https://fastapi.tiangolo.com)  
- [OpenTelemetry](https://opentelemetry.io)  
- [Prometheus](https://prometheus.io)  
- [Grafana](https://grafana.com)  
- [SHAP](https://github.com/slundberg/shap)  
- [Evidently](https://github.com/evidentlyai/evidently)  
