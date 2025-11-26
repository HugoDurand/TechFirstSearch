from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@localhost:5432/techlearning"
    redis_url: str = "redis://localhost:6379/0"
    api_host: str = "0.0.0.0"
    api_port: int = int(os.environ.get("PORT", 8000))
    log_level: str = "INFO"
    
    @property
    def celery_broker_url(self) -> str:
        return self.redis_url
    
    @property
    def celery_result_backend(self) -> str:
        return self.redis_url
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

