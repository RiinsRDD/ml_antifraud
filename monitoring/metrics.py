"""
Модуль для настройки метрик мониторинга
"""
from prometheus_client import Counter, Histogram, Gauge
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

# Создание метрик
REQUEST_COUNT = Counter(
    'antifraud_requests_total',
    'Количество запросов к сервису',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'antifraud_request_duration_seconds',
    'Время обработки запросов',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'antifraud_active_requests',
    'Активные запросы'
)

def setup_metrics(app: FastAPI):
    """
    Настройка метрик для FastAPI приложения

    Args:
        app: Экземпляр FastAPI приложения
    """
    # Установка инструмента инструментирования
    Instrumentator(
        should_group_paths=True,
        should_add_histogram=True,
        excluded_handlers=["/metrics"]
    ).instrument(app)

    # Добавление пользовательских метрик
    # (в реальном приложении могли бы быть дополнительные метрики в зависимости от бизнес-логики)

    return app

def register_custom_metrics():
    """
    Регистрация пользовательских метрик
    """
    return {
        'request_count': REQUEST_COUNT,
        'request_latency': REQUEST_LATENCY,
        'active_requests': ACTIVE_REQUESTS
    }