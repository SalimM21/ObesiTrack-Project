# ObesiTrack-Project

**ObesiTrack** — API sécurisée de prédiction de l’obésité (FastAPI + JWT + PostgreSQL + Docker + Helm).  
Ce dépôt contient une API REST prête pour dev/prod qui sert un modèle ML multiclasses pour prédire une catégorie d'obésité, avec : authentification JWT, persistance Postgres, tracing (OpenTelemetry), métriques Prometheus, endpoints d’explicabilité (SHAP) et suivi de drift (Evidently).  

---

## 📂 Contenu du dépôt
- `src/obesitrack/` : code FastAPI (API, auth, models, DB, monitoring, explainability)  
- `models/` : artefacts ML (`preprocessor.joblib`, `classifier.joblib`)  
- `docker-compose.yml` : dev (API + PostgreSQL + PgAdmin)  
- `Dockerfile` : image API  
- `helm/obesitrack/` : Helm chart minimal  
- `.github/workflows/ci.yml` : CI (lint + tests + build & push image)  
- `requirements.txt` : dépendances Python  
- `README.md` : ce document  

---

## Prérequis
- Python 3.10+  
- Docker & Docker Compose  
- Helm 3  
- Un registry Docker (Docker Hub) et secrets CI configurés  
<!-- - (Optionnel) Redis si tu veux du rate-limiting distribué   -->

---

## ⚙️ Installation & exécution locale (dev)

1. **Cloner le repo :**
```bash
git clone <repo> obesitrack && cd obesitrack
```

2. **Construire l’environnement et lancer via Docker Compose (inclut Postgres) :**
```bash
docker compose up --build
```
 API disponible sur [http://localhost:8000](http://localhost:8000)  
 Docs Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)  

3. **(Optionnel) Entraîner et sérialiser le modèle localement :**
```bash
python train.py --dataset data/obesity_levels.csv --model-dir models
```

---

##  Endpoints clés

- `POST /auth/register` — inscription utilisateur  
- `POST /auth/token` — login (OAuth2 form data) → JWT  
- `GET /auth/me` — profil courant  
- `POST /predict` — prédiction (auth requise) + enregistrement résultat  
- `GET /predictions` — historique personnel (paginé)  
- `GET /metrics` — infos du modèle  
- `GET /health` — health check  
- `POST /explain/shap` — explication SHAP (auth + rate-limit)  
- `GET /drift/report` — état drift (rapport Evidently JSON)  

---

##  Observabilité & monitoring

- **Tracing** : OpenTelemetry (OTLP exporter configurable)  
- **Metrics** : exposition Prometheus sur `/metrics`  
- **Dashboard** : Grafana (JSON minimal disponible dans `docs/grafana-dashboard.json`)  

---

##  CI / CD

- `.github/workflows/ci.yml` :  
  - Lint (flake8)  
  - Tests (pytest)  
  - Docker build & push (utilise secrets DockerHub)  

---

##  Helm chart (Kubernetes)

Fichiers prêts dans `helm/obesitrack/` pour une installation simple :  
```bash
helm install obesitrack helm/obesitrack --namespace obesitrack --create-namespace
```

---

##  Explicabilité & Drift

- **SHAP** : endpoint `/explain/shap` → génère des valeurs d’importance (limitées & mises en cache)  
- **Evidently** : script baseline + endpoint `/drift/report` (JSON de détection de drift)  

---

##  Conseils de production

- Stocker secrets dans Vault / Azure KeyVault / GCP Secret Manager  
- HTTPS + Ingress (Traefik / Nginx) + WAF  
- Mettre en place des backups PostgreSQL  
- Scanner sécurité (SAST / DAST)  

---

##  Références

- [FastAPI](https://fastapi.tiangolo.com)  
- [OpenTelemetry](https://opentelemetry.io)  
- [Prometheus](https://prometheus.io) / [Grafana](https://grafana.com)  
- [SHAP](https://github.com/slundberg/shap)  
- [Evidently](https://github.com/evidentlyai/evidently)  
