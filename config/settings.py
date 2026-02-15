"""
Конфигурация приложения
"""
import os
from typing import Optional

class Settings:
    # Redis настройки
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # Время жизни кэша в секундах (24 часа)
    CACHE_TTL: int = 24 * 60 * 60

    # Настройки логирования
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Настройки производительности
    MAX_PROCESSING_TIME_MS: int = 200  # Максимальное время обработки в миллисекундах

    # Настройки ML модели
    ML_MODEL_TIMEOUT_MS: int = 100  # Таймаут для модели в миллисекундах
    DEFAULT_SCORING_VALUE: float = 0.5  # Значение по умолчанию в случае таймаута

    # Настройки API
    API_V1_STR: str = "/api/v1"

    # Настройки безопасности
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")

# Создание экземпляра конфигурации
settings = Settings()