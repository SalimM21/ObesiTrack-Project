from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	DATABASE_URL: str = "sqlite+aiosqlite:///./obesitrack.db"
	SECRET_KEY: str = "change-me"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
	ALGORITHM: str = "HS256"

	model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

settings = Settings()
