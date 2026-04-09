from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # .env dosyasındaki değişken adlarıyla birebir aynı olmalı!
    DB_SERVER: str
    DB_NAME: str
    DB_DRIVER: str
    
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Pydantic'e bu ayarların hangi dosyadan okunacağını söylüyoruz:
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# Ayarları her yerde kullanabilmek için tek bir nesne oluşturuyoruz:
settings = Settings()
