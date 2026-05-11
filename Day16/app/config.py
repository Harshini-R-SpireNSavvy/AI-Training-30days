from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Relative URLs resolve from the process cwd — run `uvicorn` from the Day16 folder.
    database_url: str = "sqlite:///./day16_local.db"
    chroma_path: str = str(_ROOT / "chroma_data")


settings = Settings()
