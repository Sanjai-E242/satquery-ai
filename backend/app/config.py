import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SATQUERY AI"
    API_V1_STR: str = "/api"
    VERSION: str = "1.0.0"
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    BIGEARTHNET_PATH_ENV: str = ""
    
    DEMO_MODE: bool = True
    MODEL_DEVICE: str = "auto"
    MAX_UPLOAD_SIZE_MB: int = 50
    DATABASE_URL: str = ""
    
    # Production Networking & CORS
    FRONTEND_URL: str = ""
    BACKEND_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def DATA_ROOT(self) -> Path:
        return self.BASE_DIR / "data"

    @property
    def BIGEARTHNET_PATH(self) -> Path:
        if self.BIGEARTHNET_PATH_ENV:
            return Path(self.BIGEARTHNET_PATH_ENV)
        return self.DATA_ROOT / "BigEarthNet" / "BigEarthNet.txt.parquet"

    @property
    def STORAGE_DIR(self) -> Path:
        return self.BASE_DIR / "storage"

    @property
    def UPLOADS_DIR(self) -> Path:
        return self.STORAGE_DIR / "uploads"

    @property
    def GENERATED_DIR(self) -> Path:
        return self.STORAGE_DIR / "generated"

    @property
    def OUTPUTS_DIR(self) -> Path:
        return self.BASE_DIR / "outputs"

settings = Settings()

# Ensure directories exist
for path in [settings.DATA_ROOT, settings.STORAGE_DIR, settings.UPLOADS_DIR, settings.GENERATED_DIR, settings.OUTPUTS_DIR]:
    os.makedirs(path, exist_ok=True)
