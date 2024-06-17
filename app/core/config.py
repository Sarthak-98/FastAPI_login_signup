from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    # Project name
    PROJECT_NAME: str
    # List of CORS (Cross-Origin Resource Sharing) origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Validator for assembling CORS origins
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Validator to normalize CORS origins.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # PostgreSQL database configuration
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[PostgresDsn] = None
    
    # JWT (JSON Web Token) configuration
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_SECRET_KEY: str
    JWT_REFRESH_TOKEN_ACCESS_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Validator for assembling database connection URI
    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Validator to assemble PostgreSQL connection URI.
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        """
        Configuration settings for the Settings class.
        """
        case_sensitive = True  # Settings are case-sensitive
        env_file = ".env"  # Load settings from .env file

# Create an instance of the Settings class
settings = Settings()
