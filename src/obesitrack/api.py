from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import pandas as pd
from .schemas import PredictRequest, PredictResponse
from .security import get_current_user, token_endpoint
from .model import registry
from .logging_conf import setup_logging


setup_logging()

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute", "1000/hour"]) # ajustez selon besoin

middleware = [
Middleware(GZipMiddleware, minimum_size=500),
Middleware(SessionMiddleware, secret_key="dummy"),
]

app = FastAPI(title="ObesiTrack API", version="1.0.0", middleware=middleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.state

