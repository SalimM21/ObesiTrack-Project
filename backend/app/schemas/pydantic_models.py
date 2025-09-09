from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    user_id: Optional[int] = None
    role: Optional[str] = None

class PredictionIn(BaseModel):
    # add your real features: age, glucose, bmi, etc.
    age: int
    glucose: float
    bmi: float
    bloodpressure: float
    pedigree: float
    sex: Optional[str] = None

class PredictionOut(BaseModel):
    result: str
    probability: Dict[str, float]

# src/obesitrack/db_models.py
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = sa.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    username = sa.Column(sa.String(128), unique=True, nullable=False, index=True)
    email = sa.Column(sa.String(256), unique=True, nullable=False, index=True)
    password_hash = sa.Column(sa.String(256), nullable=False)
    role = sa.Column(sa.String(32), nullable=False, default="user")
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)

class Prediction(Base):
    __tablename__ = "predictions"
    id = sa.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = sa.Column(sa.String, sa.ForeignKey("users.id"), nullable=False, index=True)
    input_json = sa.Column(JSONB, nullable=False)
    predicted_label = sa.Column(sa.String(128), nullable=False)
    probabilities = sa.Column(JSONB, nullable=False)
    model_name = sa.Column(sa.String(128))
    model_version = sa.Column(sa.String(64))
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow, index=True)

from pathlib import Path
import joblib
from sklearn.base import BaseEstimator
from .config import settings


class ModelBundle:
	def __init__(self, preprocessor: BaseEstimator, classifier: BaseEstimator):
		self.preprocessor = preprocessor
		self.classifier = classifier

	def predict_proba(self, X_df):
		X_proc = self.preprocessor.transform(X_df)
		return self.classifier.predict_proba(X_proc)

	def predict(self, X_df):
		X_proc = self.preprocessor.transform(X_df)
		return self.classifier.predict(X_proc)


class ModelRegistry:
	def __init__(self, model_dir: str | Path | None = None):
		self.model_dir = Path(model_dir or settings.MODEL_DIR)
		self.preprocessor_path = self.model_dir / "preprocessor.joblib"
		self.classifier_path = self.model_dir / "classifier.joblib"
		self._bundle: ModelBundle | None = None

	def load(self) -> ModelBundle:
		if self._bundle is None:
			pre = joblib.load(self.preprocessor_path)
			clf = joblib.load(self.classifier_path)
			self._bundle = ModelBundle(pre, clf)
		return self._bundle

registry = ModelRegistry()