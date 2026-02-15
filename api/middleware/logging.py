"""
Middleware для логирования запросов
"""
from fastapi import Request
from fastapi.middleware.logging import LoggingMiddleware
import time
from loguru import logger

class AntifraudLoggingMiddleware(LoggingMiddleware):
    """Кастомное middleware для логирования запросов с метриками"""

    def __init__(self, app):
        super().__init__(app)

    async def __call__(self, request: Request, call_next):
        # Логирование входящего запроса
        start_time = time.time()

        # Логируем начало обработки
        logger.info(f"Начало обработки запроса: {request.method} {request.url}")

        try:
            response = await call_next(request)
            # Логируем завершение обработки
            process_time = (time.time() - start_time) * 1000
            logger.info(f"Завершение обработки запроса: {request.method} {request.url} - {process_time:.2f}ms")
            return response
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(f"Ошибка обработки запроса: {request.method} {request.url} - {process_time:.2f}ms - {str(e)}")
            raise