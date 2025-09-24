# ========================
#  Stage 1 - Build
# ========================
FROM python:3.10-slim AS builder

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Créer dossier app
WORKDIR /app

# Copier requirements
COPY requirements.txt .

# Installer deps en cache
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ========================
#  Stage 2 - Runtime
# ========================
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Installer dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copier deps depuis builder
COPY --from=builder /wheels /wheels
# COPY --from=builder /requirements.txt .
RUN pip install --no-cache /wheels/*

# Copier code source
COPY src/obesitrack ./src/obesitrack
COPY models ./models

# Exposer port API
EXPOSE 8000

# Lancement via gunicorn + uvicorn
CMD ["gunicorn", "src.obesitrack.main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
