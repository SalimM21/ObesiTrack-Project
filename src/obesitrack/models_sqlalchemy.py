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
