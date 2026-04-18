from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "KitchenStock AI"
    debug: bool = True
    version: str = "2.0.0"
    low_stock_threshold: float = 200.0

    # PostgreSQL
    database_url: str = "postgresql://postgres:password@localhost:5432/kitcheniq"

    # JWT
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    class Config:
        env_file = ".env"

settings = Settings()
