from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    debug: bool
    version: str
    low_stock_threshold: float

    class Config:
        env_file = ".env"

settings = Settings()