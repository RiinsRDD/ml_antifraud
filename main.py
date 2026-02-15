"""
Микросервис оценки финансовых транзакций
"""
import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.logging import LoggingMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from api.routes.transaction import router as transaction_router
from config.settings import settings
from utils.logger import setup_logger
from monitoring.metrics import setup_metrics

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

# Добавление middleware для логирования
app.add_middleware(LoggingMiddleware)

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