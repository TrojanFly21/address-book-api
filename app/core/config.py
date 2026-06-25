from pydantic import BaseModel


class Settings(BaseModel):
    """
    Application configuration settings.

    Centralizes configurable values such as the application metadata
    and database connection string.
    """
    APP_NAME: str = "Address Book API"
    APP_VERSION: str = "1.0.0"
    
    # SQLite database connection URL.
    DATABASE_URL: str = "sqlite:///./address_book.db"

# Global settings instance used throughout the application.
settings = Settings()