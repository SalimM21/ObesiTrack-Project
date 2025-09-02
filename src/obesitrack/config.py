from pydantic import BaseModel, BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	SECRET_KEY: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
	ALGORITHM: str = "HS256"
	MODEL_DIR: str = "models"
	ADMIN_USERNAME: str = "admin"
	ADMIN_PASSWORD_HASH: str


model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()