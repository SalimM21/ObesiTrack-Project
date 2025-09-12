from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.api import users, predictions, auth, metrics


# Optional logging/observability setup (disabled if modules missing)
# from logging_conf import setup_logging
# from observability import init_tracing
# setup_logging()

middleware = [
    Middleware(GZipMiddleware, minimum_size=500),
]

app = FastAPI(title="ObesiTrack API", version="1.0.0", middleware=middleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# try:
#     init_tracing(app, service_name="obesitrack")
# except Exception:
#     pass

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(metrics.router)

# Healthcheck
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenue sur l'API ObesiTrack 🚀"}


