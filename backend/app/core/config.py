from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	DATABASE_URL: str = "sqlite+aiosqlite:///./obesitrack.db"
	SECRET_KEY: str = "change-me"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
	ALGORITHM: str = "HS256"

	model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    admin_username: str
    admin_password_hash: str

    model_dir: str
    grafana_url: str
    grafana_api_key: str
    grafana_dashboard_uid: str

    class Config:
        env_file = ".env"
        extra = "allow"  # <-- important si tu veux ignorer les variables non définies

