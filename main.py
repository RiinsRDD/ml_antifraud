"""
Микросервис оценки финансовых транзакций
"""
import asyncio
import logging
from fastapi import FastAPI, Depends
from prometheus_fastapi_instrumentator import Instrumentator
from api.routes.transaction import router as transaction_router
from config.settings import settings
from utils.logger import setup_logger
from monitoring.metrics import setup_metrics
from services.transaction_service_impl import TransactionServiceImpl
from services.scoring_service_impl import ScoringServiceImpl
from repositories.redis_transaction_repository import RedisTransactionRepository

# Инициализация логгера
logger = setup_logger(__name__)

# Создание экземпляра приложения FastAPI
app = FastAPI(
    title="Antifraud Scoring Service",
    description="Микросервис для оценки финансовых транзакций",
    version="0.1.0"
)

# Настройка инструментов мониторинга
setup_metrics(app)

# =============================================================================
# Dependency Injection Providers
# =============================================================================

# Хранилище для singleton объектов
_app_state = {}


def get_redis_repository() -> RedisTransactionRepository:
    """Провайдер для Redis репозитория"""
    if "redis_repository" not in _app_state:
        _app_state["redis_repository"] = RedisTransactionRepository(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD
        )
    return _app_state["redis_repository"]


def get_scoring_service() -> ScoringServiceImpl:
    """Провайдер для сервиса оценки"""
    if "scoring_service" not in _app_state:
        _app_state["scoring_service"] = ScoringServiceImpl()
    return _app_state["scoring_service"]


def get_transaction_service() -> TransactionServiceImpl:
    """Провайдер для сервиса транзакций"""
    repository = get_redis_repository()
    scoring_service = get_scoring_service()
    return TransactionServiceImpl(
        repository=repository,
        scoring_service=scoring_service
    )


# Регистрация маршрутов
app.include_router(transaction_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Событие запуска приложения"""
    logger.info("Запуск микросервиса оценки транзакций")
    # Здесь можно инициализировать соединения с базами данных, кэшами и т.д.
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """Событие остановки приложения"""
    logger.info("Остановка микросервиса оценки транзакций")
    # Здесь можно закрывать соединения, очищать ресурсы и т.д.
    pass

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Микросервис оценки финансовых транзакций запущен"}

@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    """Эндпоинт метрик Prometheus"""
    from prometheus_client import generate_latest
    return generate_latest()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)