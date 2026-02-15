This file is a merged representation of a subset of the codebase, containing specifically included files and files not matching ignore patterns, combined into a single document by Repomix.
The content has been processed where line numbers have been added.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: **/*
- Files matching these patterns are excluded: **/venv/**, **/.venv/**, **/__pycache__/**, **/.pytest_cache/**, **/.mypy_cache/**, **/.git/**, **/migrations/**, *.log, *.pyc, README.md, *repomix.config.json, .gitignore
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Line numbers have been added to the beginning of each line
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
api/
  middleware/
    logging.py
  routes/
    transaction.py
config/
  settings.py
exceptions/
  __init__.py
load_generator/
  traffic_generator.py
models/
  scoring.py
  transaction.py
monitoring/
  metrics.py
repositories/
  transaction_repository.py
services/
  scoring_service.py
  transaction_service.py
tests/
  test_models.py
  test_services.py
utils/
  logger.py
ai.md
ARCHITECTURE.md
docker-compose.traffic.yaml
docker-compose.yaml
Dockerfile
main.py
prometheus.yml
pyproject.toml
```

# Files

## File: api/middleware/logging.py
````python
 1: """
 2: Middleware для логирования запросов
 3: """
 4: from fastapi import Request
 5: from fastapi.middleware.logging import LoggingMiddleware
 6: import time
 7: from loguru import logger
 8: 
 9: class AntifraudLoggingMiddleware(LoggingMiddleware):
10:     """Кастомное middleware для логирования запросов с метриками"""
11: 
12:     def __init__(self, app):
13:         super().__init__(app)
14: 
15:     async def __call__(self, request: Request, call_next):
16:         # Логирование входящего запроса
17:         start_time = time.time()
18: 
19:         # Логируем начало обработки
20:         logger.info(f"Начало обработки запроса: {request.method} {request.url}")
21: 
22:         try:
23:             response = await call_next(request)
24:             # Логируем завершение обработки
25:             process_time = (time.time() - start_time) * 1000
26:             logger.info(f"Завершение обработки запроса: {request.method} {request.url} - {process_time:.2f}ms")
27:             return response
28:         except Exception as e:
29:             process_time = (time.time() - start_time) * 1000
30:             logger.error(f"Ошибка обработки запроса: {request.method} {request.url} - {process_time:.2f}ms - {str(e)}")
31:             raise
````

## File: api/routes/transaction.py
````python
 1: """
 2: API маршруты для работы с транзакциями
 3: """
 4: from fastapi import APIRouter, HTTPException, Depends
 5: from typing import Optional
 6: from models.transaction import Transaction
 7: from models.scoring import ScoringResult
 8: from services.transaction_service import TransactionService
 9: from config.settings import settings
10: from utils.logger import setup_logger
11: 
12: logger = setup_logger(__name__)
13: 
14: router = APIRouter(prefix="/transactions", tags=["transactions"])
15: 
16: @router.post("/", response_model=ScoringResult, status_code=200)
17: async def process_transaction(
18:     transaction: Transaction,
19:     transaction_service: TransactionService = Depends()
20: ):
21:     """
22:     Обработать транзакцию и вернуть оценку риска
23: 
24:     Args:
25:         transaction: Входящая транзакция
26:         transaction_service: Сервис обработки транзакций
27: 
28:     Returns:
29:         Результат оценки транзакции
30: 
31:     Raises:
32:         HTTPException: Если произошла ошибка обработки
33:     """
34:     logger.info(f"Получена транзакция: {transaction.transaction_id} от клиента: {transaction.customer_id}")
35: 
36:     try:
37:         # Обработка транзакции
38:         result = await transaction_service.process_transaction(transaction)
39:         logger.info(f"Оценка транзакции {transaction.transaction_id} завершена. Результат: {result.scoring}")
40:         return result
41:     except Exception as e:
42:         logger.error(f"Ошибка обработки транзакции {transaction.transaction_id}: {str(e)}")
43:         raise HTTPException(status_code=500, detail=f"Ошибка обработки транзакции: {str(e)}")
````

## File: config/settings.py
````python
 1: """
 2: Конфигурация приложения
 3: """
 4: import os
 5: from typing import Optional
 6: 
 7: class Settings:
 8:     # Redis настройки
 9:     REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
10:     REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
11:     REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
12:     REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
13: 
14:     # Время жизни кэша в секундах (24 часа)
15:     CACHE_TTL: int = 24 * 60 * 60
16: 
17:     # Настройки логирования
18:     LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
19: 
20:     # Настройки производительности
21:     MAX_PROCESSING_TIME_MS: int = 200  # Максимальное время обработки в миллисекундах
22: 
23:     # Настройки ML модели
24:     ML_MODEL_TIMEOUT_MS: int = 100  # Таймаут для модели в миллисекундах
25:     DEFAULT_SCORING_VALUE: float = 0.5  # Значение по умолчанию в случае таймаута
26: 
27:     # Настройки API
28:     API_V1_STR: str = "/api/v1"
29: 
30:     # Настройки безопасности
31:     SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
32: 
33: # Создание экземпляра конфигурации
34: settings = Settings()
````

## File: exceptions/__init__.py
````python
 1: """
 2: Пользовательские исключения
 3: """
 4: 
 5: class AntifraudException(Exception):
 6:     """Базовое исключение для антифрод сервиса"""
 7:     pass
 8: 
 9: class TransactionProcessingError(AntifraudException):
10:     """Ошибка обработки транзакции"""
11:     pass
12: 
13: class ModelTimeoutError(AntifraudException):
14:     """Ошибка таймаута модели"""
15:     pass
16: 
17: class CacheError(AntifraudException):
18:     """Ошибка кэширования"""
19:     pass
````

## File: load_generator/traffic_generator.py
````python
  1: """
  2: Генератор трафика для микросервиса антифрод оценки транзакций
  3: Использует asyncio для асинхронной генерации нагрузки
  4: """
  5: import asyncio
  6: import random
  7: import json
  8: import time
  9: from datetime import datetime, timedelta
 10: import aiohttp
 11: from typing import Dict, Any
 12: from loguru import logger
 13: 
 14: 
 15: class TrafficGenerator:
 16:     """Класс для генерации трафика"""
 17: 
 18:     def __init__(self, base_url: str = "http://localhost:8000", max_transactions: int = 1000):
 19:         """
 20:         Инициализация генератора трафика
 21: 
 22:         Args:
 23:             base_url: Базовый URL сервиса
 24:             max_transactions: Максимальное количество транзакций в секунду
 25:         """
 26:         self.base_url = base_url
 27:         self.max_transactions = max_transactions
 28:         self.session = None
 29:         self.running = False
 30:         self.total_transactions = 0
 31:         self.errors = 0
 32: 
 33:     async def __aenter__(self):
 34:         """Async context manager entry"""
 35:         self.session = aiohttp.ClientSession()
 36:         return self
 37: 
 38:     async def __aexit__(self, exc_type, exc_val, exc_tb):
 39:         """Async context manager exit"""
 40:         if self.session:
 41:             await self.session.close()
 42: 
 43:     def _generate_random_transaction(self) -> Dict[str, Any]:
 44:         """
 45:         Генерация случайной транзакции
 46: 
 47:         Returns:
 48:             Словарь с данными транзакции
 49:         """
 50:         # Список возможных типов транзакций
 51:         transaction_types = [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
 52: 
 53:         # Список возможных валют
 54:         currencies = ['USD', 'EUR', 'RUB', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF']
 55: 
 56:         # Список возможных каналов
 57:         channels = ['online', 'mobile', 'pos', 'atm']
 58: 
 59:         # Список возможных локаций
 60:         locations = ['US-NY', 'US-CA', 'US-TX', 'US-FL', 'US-WA', 'GB-LON', 'DE-BER', 'FR-PAR', 'JP-TOK', 'CN-BEI']
 61: 
 62:         # Генерация случайных данных
 63:         transaction = {
 64:             "customer_id": f"customer_{random.randint(1, 100000)}",
 65:             "transaction_id": f"txn_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
 66:             "amount": round(random.uniform(1.0, 10000.0), 2),
 67:             "type": random.choice(transaction_types),
 68:             "currency": random.choice(currencies),
 69:             "timestamp": datetime.utcnow().isoformat() + "Z",
 70:             "merchant_id": f"merchant_{random.randint(1, 10000)}",
 71:             "card_bin": f"{random.randint(100000, 999999)}",
 72:             "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
 73:             "device_id": f"device_{random.randint(1, 1000000)}",
 74:             "location": random.choice(locations),
 75:             "channel": random.choice(channels),
 76:             "merchant_risk_score": round(random.uniform(0.0, 1.0), 3),
 77:             "card_risk_score": round(random.uniform(0.0, 1.0), 3),
 78:             "customer_risk_score": round(random.uniform(0.0, 1.0), 3),
 79:             "is_velocity_alert": random.choice([True, False]),
 80:             "is_location_alert": random.choice([True, False]),
 81:             "is_device_alert": random.choice([True, False]),
 82:             "transaction_category": random.choice(['ecommerce', 'retail', 'atm', 'card', 'mobile', 'wire']),
 83:             "is_high_value": random.choice([True, False])
 84:         }
 85: 
 86:         return transaction
 87: 
 88:     async def send_transaction(self, transaction_data: Dict[str, Any]) -> bool:
 89:         """
 90:         Отправка одной транзакции
 91: 
 92:         Args:
 93:             transaction_data: Данные транзакции
 94: 
 95:         Returns:
 96:             True если успешно, False в случае ошибки
 97:         """
 98:         try:
 99:             url = f"{self.base_url}/api/v1/transactions"
100:             async with self.session.post(url, json=transaction_data, timeout=5) as response:
101:                 if response.status == 200:
102:                     result = await response.json()
103:                     logger.debug(f"Успешно обработана транзакция: {result['transaction_id']}")
104:                     return True
105:                 else:
106:                     logger.error(f"Ошибка при отправке транзакции: {response.status}")
107:                     return False
108:         except Exception as e:
109:             logger.error(f"Исключение при отправке транзакции: {str(e)}")
110:             return False
111: 
112:     async def generate_traffic(self, duration_seconds: int = 60):
113:         """
114:         Генерация трафика в течение заданного времени
115: 
116:         Args:
117:             duration_seconds: Длительность генерации в секундах
118:         """
119:         logger.info(f"Запуск генератора трафика на {duration_seconds} секунд")
120: 
121:         start_time = time.time()
122:         self.running = True
123: 
124:         try:
125:             while self.running and (time.time() - start_time) < duration_seconds:
126:                 # Рассчитываем количество транзакций в этом периоде
127:                 transactions_per_second = min(self.max_transactions, 1000)
128: 
129:                 # Генерируем транзакции
130:                 tasks = []
131:                 for _ in range(transactions_per_second):
132:                     transaction = self._generate_random_transaction()
133:                     task = self.send_transaction(transaction)
134:                     tasks.append(task)
135: 
136:                 # Выполняем все запросы параллельно
137:                 results = await asyncio.gather(*tasks, return_exceptions=True)
138: 
139:                 # Считаем ошибки и успешные запросы
140:                 for result in results:
141:                     if isinstance(result, bool) and result:
142:                         self.total_transactions += 1
143:                     elif not isinstance(result, bool) or not result:
144:                         self.errors += 1
145: 
146:                 # Вывод статистики каждые 10 секунд
147:                 if int(time.time() - start_time) % 10 == 0:
148:                     logger.info(f"Статистика: {self.total_transactions} транзакций, {self.errors} ошибок")
149: 
150:                 # Задержка для ограничения скорости (сохраняем нужное количество транзакций в секунду)
151:                 await asyncio.sleep(1)
152: 
153:         except KeyboardInterrupt:
154:             logger.info("Генерация трафика прервана пользователем")
155:         except Exception as e:
156:             logger.error(f"Ошибка в генерации трафика: {str(e)}")
157:         finally:
158:             self.running = False
159:             logger.info(f"Генерация трафика завершена. Всего: {self.total_transactions} транзакций, ошибок: {self.errors}")
160: 
161:     def stop(self):
162:         """Остановка генерации трафика"""
163:         self.running = False
164: 
165:     def get_stats(self) -> Dict[str, Any]:
166:         """
167:         Получение статистики генерации трафика
168: 
169:         Returns:
170:             Словарь со статистикой
171:         """
172:         return {
173:             "total_transactions": self.total_transactions,
174:             "errors": self.errors,
175:             "success_rate": self.total_transactions / (self.total_transactions + self.errors) if (self.total_transactions + self.errors) > 0 else 0
176:         }
177: 
178: 
179: async def main():
180:     """Основная функция для запуска генератора трафика"""
181:     async with TrafficGenerator(max_transactions=1000) as generator:
182:         await generator.generate_traffic(duration_seconds=60)
183: 
184: 
185: if __name__ == "__main__":
186:     asyncio.run(main())
````

## File: models/scoring.py
````python
 1: """
 2: Модели результатов оценки
 3: """
 4: from pydantic import BaseModel, Field
 5: from typing import Optional
 6: from datetime import datetime
 7: 
 8: class ScoringResult(BaseModel):
 9:     """Результат оценки транзакции"""
10: 
11:     # Обязательные поля из входной транзакции
12:     customer_id: str = Field(..., description="ID клиента")
13:     transaction_id: str = Field(..., description="ID транзакции")
14: 
15:     # Поле оценки
16:     scoring: float = Field(..., description="Оценка риска транзакции от 0 до 1")
17: 
18:     # Дополнительные поля для анализа
19:     is_fraud: Optional[bool] = Field(None, description="Флаг мошенничества (по оценке)")
20:     processing_time_ms: Optional[int] = Field(None, description="Время обработки в миллисекундах")
21: 
22:     # Статистика по клиенту
23:     customer_transaction_count_24h: Optional[int] = Field(None, description="Количество транзакций за 24 часа")
24:     customer_avg_amount_24h: Optional[float] = Field(None, description="Средняя сумма за 24 часа")
25:     customer_transaction_count_3h: Optional[int] = Field(None, description="Количество транзакций за 3 часа")
26:     customer_avg_amount_3h: Optional[float] = Field(None, description="Средняя сумма за 3 часа")
27:     customer_transaction_count_6h: Optional[int] = Field(None, description="Количество транзакций за 6 часов")
28:     customer_avg_amount_6h: Optional[float] = Field(None, description="Средняя сумма за 6 часов")
29:     customer_transaction_count_12h: Optional[int] = Field(None, description="Количество транзакций за 12 часов")
30:     customer_avg_amount_12h: Optional[float] = Field(None, description="Средняя сумма за 12 часов")
31: 
32:     # Временные метки
33:     processed_at: str = Field(..., description="Время обработки")
34: 
35:     class Config:
36:         """Конфигурация модели"""
37:         schema_extra = {
38:             "example": {
39:                 "customer_id": "customer_123",
40:                 "transaction_id": "txn_456",
41:                 "scoring": 0.25,
42:                 "is_fraud": False,
43:                 "processing_time_ms": 85,
44:                 "customer_transaction_count_24h": 15,
45:                 "customer_avg_amount_24h": 75.25,
46:                 "customer_transaction_count_3h": 2,
47:                 "customer_avg_amount_3h": 100.0,
48:                 "customer_transaction_count_6h": 5,
49:                 "customer_avg_amount_6h": 90.5,
50:                 "customer_transaction_count_12h": 8,
51:                 "customer_avg_amount_12h": 85.75,
52:                 "processed_at": "2023-01-01T10:00:00Z"
53:             }
54:         }
````

## File: models/transaction.py
````python
 1: """
 2: Модели транзакций
 3: """
 4: from pydantic import BaseModel, Field
 5: from typing import Optional, List
 6: from datetime import datetime
 7: 
 8: class Transaction(BaseModel):
 9:     """Модель финансовой транзакции"""
10: 
11:     # Обязательные поля
12:     customer_id: str = Field(..., description="ID клиента")
13:     transaction_id: str = Field(..., description="ID транзакции")
14: 
15:     # Основные финансовые данные
16:     amount: float = Field(..., description="Сумма транзакции")
17:     currency: str = Field(..., description="Валюта транзакции")
18:     type: int = Field(..., description="Тип транзакции")
19: 
20:     # Дополнительные поля для анализа
21:     merchant_id: str = Field(..., description="ID мерчанта")
22:     card_bin: str = Field(..., description="BIN номер карты")
23:     ip_address: str = Field(..., description="IP адрес клиента")
24:     device_id: str = Field(..., description="ID устройства")
25:     location: str = Field(..., description="Местоположение")
26:     channel: str = Field(..., description="Канал транзакции")
27: 
28:     # Временные метки
29:     timestamp: str = Field(..., description="Временная метка транзакции")
30: 
31:     # Поля для анализа
32:     is_fraud: Optional[bool] = Field(None, description="Флаг мошенничества")
33:     merchant_risk_score: Optional[float] = Field(None, description="Рейтинг риска мерчанта")
34:     card_risk_score: Optional[float] = Field(None, description="Рейтинг риска карты")
35:     customer_risk_score: Optional[float] = Field(None, description="Рейтинг риска клиента")
36: 
37:     # Дополнительные поля
38:     is_velocity_alert: Optional[bool] = Field(None, description="Оповещение о скорости транзакций")
39:     is_location_alert: Optional[bool] = Field(None, description="Оповещение о геолокации")
40:     is_device_alert: Optional[bool] = Field(None, description="Оповещение об устройстве")
41: 
42:     # Поля для будущего использования
43:     customer_segments: Optional[List[str]] = Field(None, description="Сегменты клиента")
44:     transaction_category: Optional[str] = Field(None, description="Категория транзакции")
45:     is_high_value: Optional[bool] = Field(None, description="Высокая стоимость транзакции")
46: 
47:     class Config:
48:         """Конфигурация модели"""
49:         schema_extra = {
50:             "example": {
51:                 "customer_id": "customer_123",
52:                 "transaction_id": "txn_456",
53:                 "amount": 100.50,
54:                 "currency": "USD",
55:                 "type": 78,
56:                 "merchant_id": "merchant_789",
57:                 "card_bin": "411111",
58:                 "ip_address": "192.168.1.1",
59:                 "device_id": "device_001",
60:                 "location": "US-NY",
61:                 "channel": "online",
62:                 "timestamp": "2023-01-01T10:00:00Z",
63:                 "is_fraud": False,
64:                 "merchant_risk_score": 0.2,
65:                 "card_risk_score": 0.1,
66:                 "customer_risk_score": 0.3,
67:             }
68:         }
````

## File: monitoring/metrics.py
````python
 1: """
 2: Модуль для настройки метрик мониторинга
 3: """
 4: from prometheus_client import Counter, Histogram, Gauge
 5: from fastapi import FastAPI
 6: from prometheus_fastapi_instrumentator import Instrumentator
 7: 
 8: # Создание метрик
 9: REQUEST_COUNT = Counter(
10:     'antifraud_requests_total',
11:     'Количество запросов к сервису',
12:     ['method', 'endpoint', 'status_code']
13: )
14: 
15: REQUEST_LATENCY = Histogram(
16:     'antifraud_request_duration_seconds',
17:     'Время обработки запросов',
18:     ['method', 'endpoint']
19: )
20: 
21: ACTIVE_REQUESTS = Gauge(
22:     'antifraud_active_requests',
23:     'Активные запросы'
24: )
25: 
26: def setup_metrics(app: FastAPI):
27:     """
28:     Настройка метрик для FastAPI приложения
29: 
30:     Args:
31:         app: Экземпляр FastAPI приложения
32:     """
33:     # Установка инструмента инструментирования
34:     Instrumentator(
35:         should_group_paths=True,
36:         should_add_histogram=True,
37:         excluded_handlers=["/metrics"]
38:     ).instrument(app)
39: 
40:     # Добавление пользовательских метрик
41:     # (в реальном приложении могли бы быть дополнительные метрики в зависимости от бизнес-логики)
42: 
43:     return app
44: 
45: def register_custom_metrics():
46:     """
47:     Регистрация пользовательских метрик
48:     """
49:     return {
50:         'request_count': REQUEST_COUNT,
51:         'request_latency': REQUEST_LATENCY,
52:         'active_requests': ACTIVE_REQUESTS
53:     }
````

## File: repositories/transaction_repository.py
````python
 1: """
 2: Репозиторий для работы с транзакциями в Redis
 3: """
 4: from abc import ABC, abstractmethod
 5: from typing import List, Dict, Optional
 6: from models.transaction import Transaction
 7: 
 8: class TransactionRepository(ABC):
 9:     """Абстрактный базовый класс репозитория транзакций"""
10: 
11:     @abstractmethod
12:     async def add_transaction(self, transaction: Transaction) -> None:
13:         """
14:         Добавить транзакцию в кэш
15: 
16:         Args:
17:             transaction: Транзакция для добавления
18: 
19:         Raises:
20:             NotImplementedError: Если метод не реализован
21:         """
22:         ...
23: 
24:     @abstractmethod
25:     async def get_transactions_by_customer(self, customer_id: str) -> List[Transaction]:
26:         """
27:         Получить все транзакции по customer_id
28: 
29:         Args:
30:             customer_id: ID клиента
31: 
32:         Returns:
33:             Список транзакций
34: 
35:         Raises:
36:             NotImplementedError: Если метод не реализован
37:         """
38:         ...
39: 
40:     @abstractmethod
41:     async def get_statistics_by_customer(self, customer_id: str) -> Dict:
42:         """
43:         Получить статистику по customer_id
44: 
45:         Args:
46:             customer_id: ID клиента
47: 
48:         Returns:
49:             Словарь со статистикой
50: 
51:         Raises:
52:             NotImplementedError: Если метод не реализован
53:         """
54:         ...
55: 
56:     @abstractmethod
57:     async def update_statistics(self, customer_id: str, stats: Dict) -> None:
58:         """
59:         Обновить статистику по customer_id
60: 
61:         Args:
62:             customer_id: ID клиента
63:             stats: Статистика для обновления
64: 
65:         Raises:
66:             NotImplementedError: Если метод не реализован
67:         """
68:         ...
69: 
70:     @abstractmethod
71:     async def get_cached_transaction(self, customer_id: str) -> Optional[Transaction]:
72:         """
73:         Получить транзакцию по customer_id из кэша
74: 
75:         Args:
76:             customer_id: ID клиента
77: 
78:         Returns:
79:             Транзакция или None
80: 
81:         Raises:
82:             NotImplementedError: Если метод не реализован
83:         """
84:         ...
85: 
86:     @abstractmethod
87:     async def delete_expired_transactions(self) -> None:
88:         """
89:         Удалить истекшие транзакции из кэша
90: 
91:         Raises:
92:             NotImplementedError: Если метод не реализован
93:         """
94:         ...
````

## File: services/scoring_service.py
````python
 1: """
 2: Сервис оценки транзакций с использованием ML модели
 3: """
 4: from abc import ABC, abstractmethod
 5: from typing import Optional
 6: from models.transaction import Transaction
 7: from models.scoring import ScoringResult
 8: 
 9: class ScoringService(ABC):
10:     """Абстрактный базовый класс сервиса оценки"""
11: 
12:     @abstractmethod
13:     async def score_transaction(self, transaction: Transaction) -> ScoringResult:
14:         """
15:         Оценить транзакцию с помощью ML модели
16: 
17:         Args:
18:             transaction: Транзакция для оценки
19: 
20:         Returns:
21:             Результат оценки транзакции
22: 
23:         Raises:
24:             NotImplementedError: Если метод не реализован
25:         """
26:         ...
27: 
28:     @abstractmethod
29:     async def _get_ml_model_score(self, transaction: Transaction) -> float:
30:         """
31:         Получить оценку от ML модели
32: 
33:         Args:
34:             transaction: Транзакция для оценки
35: 
36:         Returns:
37:             Оценка от 0 до 1
38: 
39:         Raises:
40:             NotImplementedError: Если метод не реализован
41:         """
42:         ...
43: 
44:     @abstractmethod
45:     async def _handle_model_timeout(self, transaction: Transaction) -> float:
46:         """
47:         Обработка таймаута модели
48: 
49:         Args:
50:             transaction: Транзакция для оценки
51: 
52:         Returns:
53:             Оценка по умолчанию
54: 
55:         Raises:
56:             NotImplementedError: Если метод не реализован
57:         """
58:         ...
````

## File: services/transaction_service.py
````python
 1: """
 2: Сервис обработки транзакций
 3: """
 4: from abc import ABC, abstractmethod
 5: from typing import Optional
 6: from models.transaction import Transaction
 7: from models.scoring import ScoringResult
 8: 
 9: class TransactionService(ABC):
10:     """Абстрактный базовый класс сервиса транзакций"""
11: 
12:     @abstractmethod
13:     async def process_transaction(self, transaction: Transaction) -> ScoringResult:
14:         """
15:         Обработать транзакцию и вернуть результат оценки
16: 
17:         Args:
18:             transaction: Входящая транзакция
19: 
20:         Returns:
21:             Результат оценки транзакции
22: 
23:         Raises:
24:             NotImplementedError: Если метод не реализован
25:         """
26:         ...
27: 
28:     @abstractmethod
29:     async def _validate_transaction(self, transaction: Transaction) -> bool:
30:         """
31:         Валидация транзакции
32: 
33:         Args:
34:             transaction: Транзакция для валидации
35: 
36:         Returns:
37:             Результат валидации
38: 
39:         Raises:
40:             NotImplementedError: Если метод не реализован
41:         """
42:         ...
43: 
44:     @abstractmethod
45:     async def _calculate_statistics(self, customer_id: str) -> dict:
46:         """
47:         Расчет статистики по клиенту
48: 
49:         Args:
50:             customer_id: ID клиента
51: 
52:         Returns:
53:             Словарь со статистикой
54: 
55:         Raises:
56:             NotImplementedError: Если метод не реализован
57:         """
58:         ...
59: 
60:     @abstractmethod
61:     async def _get_processing_time(self, start_time: float, end_time: float) -> int:
62:         """
63:         Расчет времени обработки
64: 
65:         Args:
66:             start_time: Время начала
67:             end_time: Время окончания
68: 
69:         Returns:
70:             Время обработки в миллисекундах
71: 
72:         Raises:
73:             NotImplementedError: Если метод не реализован
74:         """
75:         ...
````

## File: tests/test_models.py
````python
 1: """
 2: Тесты для моделей данных
 3: """
 4: import pytest
 5: from models.transaction import Transaction
 6: from models.scoring import ScoringResult
 7: 
 8: 
 9: def test_transaction_model_valid():
10:     """Тест валидации модели транзакции"""
11:     transaction_data = {
12:         "customer_id": "customer_123",
13:         "transaction_id": "txn_456",
14:         "amount": 100.50,
15:         "currency": "USD",
16:         "type": 78,
17:         "merchant_id": "merchant_789",
18:         "card_bin": "411111",
19:         "ip_address": "192.168.1.1",
20:         "device_id": "device_001",
21:         "location": "US-NY",
22:         "channel": "online",
23:         "timestamp": "2023-01-01T10:00:00Z"
24:     }
25: 
26:     transaction = Transaction(**transaction_data)
27: 
28:     assert transaction.customer_id == "customer_123"
29:     assert transaction.transaction_id == "txn_456"
30:     assert transaction.amount == 100.50
31:     assert transaction.currency == "USD"
32:     assert transaction.type == 78
33:     assert transaction.timestamp == "2023-01-01T10:00:00Z"
34: 
35: 
36: def test_transaction_model_invalid():
37:     """Тест валидации модели транзакции с неверными данными"""
38:     transaction_data = {
39:         "customer_id": "customer_123",
40:         "amount": 100.50,  # отсутствует обязательное поле transaction_id
41:         "currency": "USD",
42:         "type": 78,
43:         "merchant_id": "merchant_789",
44:         "card_bin": "411111",
45:         "ip_address": "192.168.1.1",
46:         "device_id": "device_001",
47:         "location": "US-NY",
48:         "channel": "online",
49:         "timestamp": "2023-01-01T10:00:00Z"
50:     }
51: 
52:     with pytest.raises(Exception):  # Pydantic генерирует исключение при невалидных данных
53:         Transaction(**transaction_data)
54: 
55: 
56: def test_scoring_result_model():
57:     """Тест модели результата оценки"""
58:     scoring_data = {
59:         "customer_id": "customer_123",
60:         "transaction_id": "txn_456",
61:         "scoring": 0.25,
62:         "is_fraud": False,
63:         "processing_time_ms": 85,
64:         "customer_transaction_count_24h": 15,
65:         "customer_avg_amount_24h": 75.25,
66:         "customer_transaction_count_3h": 2,
67:         "customer_avg_amount_3h": 100.0,
68:         "customer_transaction_count_6h": 5,
69:         "customer_avg_amount_6h": 90.5,
70:         "customer_transaction_count_12h": 8,
71:         "customer_avg_amount_12h": 85.75,
72:         "processed_at": "2023-01-01T10:00:00Z"
73:     }
74: 
75:     scoring_result = ScoringResult(**scoring_data)
76: 
77:     assert scoring_result.customer_id == "customer_123"
78:     assert scoring_result.transaction_id == "txn_456"
79:     assert scoring_result.scoring == 0.25
80:     assert scoring_result.is_fraud is False
81:     assert scoring_result.processing_time_ms == 85
````

## File: tests/test_services.py
````python
  1: """
  2: Тесты для сервисов
  3: """
  4: import pytest
  5: from unittest.mock import AsyncMock, MagicMock
  6: from services.transaction_service import TransactionService
  7: from services.scoring_service import ScoringService
  8: from models.transaction import Transaction
  9: from models.scoring import ScoringResult
 10: 
 11: 
 12: class MockTransactionService(TransactionService):
 13:     """Мок для тестирования TransactionService"""
 14: 
 15:     async def process_transaction(self, transaction: Transaction) -> ScoringResult:
 16:         # Пустая реализация для тестирования
 17:         return ScoringResult(
 18:             customer_id=transaction.customer_id,
 19:             transaction_id=transaction.transaction_id,
 20:             scoring=0.5,
 21:             processed_at="2023-01-01T10:00:00Z"
 22:         )
 23: 
 24:     async def _validate_transaction(self, transaction: Transaction) -> bool:
 25:         return True
 26: 
 27:     async def _calculate_statistics(self, customer_id: str) -> dict:
 28:         return {
 29:             "transaction_count_24h": 10,
 30:             "avg_amount_24h": 100.0
 31:         }
 32: 
 33:     async def _get_processing_time(self, start_time: float, end_time: float) -> int:
 34:         return 50
 35: 
 36: 
 37: class MockScoringService(ScoringService):
 38:     """Мок для тестирования ScoringService"""
 39: 
 40:     async def score_transaction(self, transaction: Transaction) -> ScoringResult:
 41:         # Пустая реализация для тестирования
 42:         return ScoringResult(
 43:             customer_id=transaction.customer_id,
 44:             transaction_id=transaction.transaction_id,
 45:             scoring=0.5,
 46:             processed_at="2023-01-01T10:00:00Z"
 47:         )
 48: 
 49:     async def _get_ml_model_score(self, transaction: Transaction) -> float:
 50:         return 0.5
 51: 
 52:     async def _handle_model_timeout(self, transaction: Transaction) -> float:
 53:         return 0.5
 54: 
 55: 
 56: @pytest.mark.asyncio
 57: async def test_transaction_service_interface():
 58:     """Тест интерфейса TransactionService"""
 59:     service = MockTransactionService()
 60: 
 61:     # Проверяем, что методы существуют
 62:     assert hasattr(service, 'process_transaction')
 63:     assert hasattr(service, '_validate_transaction')
 64:     assert hasattr(service, '_calculate_statistics')
 65:     assert hasattr(service, '_get_processing_time')
 66: 
 67: 
 68: @pytest.mark.asyncio
 69: async def test_scoring_service_interface():
 70:     """Тест интерфейса ScoringService"""
 71:     service = MockScoringService()
 72: 
 73:     # Проверяем, что методы существуют
 74:     assert hasattr(service, 'score_transaction')
 75:     assert hasattr(service, '_get_ml_model_score')
 76:     assert hasattr(service, '_handle_model_timeout')
 77: 
 78: 
 79: @pytest.mark.asyncio
 80: async def test_transaction_service_process():
 81:     """Тест метода process_transaction"""
 82:     service = MockTransactionService()
 83: 
 84:     transaction_data = {
 85:         "customer_id": "customer_123",
 86:         "transaction_id": "txn_456",
 87:         "amount": 100.50,
 88:         "currency": "USD",
 89:         "type": 78,
 90:         "merchant_id": "merchant_789",
 91:         "card_bin": "411111",
 92:         "ip_address": "192.168.1.1",
 93:         "device_id": "device_001",
 94:         "location": "US-NY",
 95:         "channel": "online",
 96:         "timestamp": "2023-01-01T10:00:00Z"
 97:     }
 98: 
 99:     transaction = Transaction(**transaction_data)
100: 
101:     # Проверяем, что метод вызывается без ошибок
102:     result = await service.process_transaction(transaction)
103: 
104:     assert result.customer_id == "customer_123"
105:     assert result.transaction_id == "txn_456"
106:     assert result.scoring == 0.5
````

## File: utils/logger.py
````python
 1: """
 2: Настройка логгирования
 3: """
 4: import sys
 5: from loguru import logger
 6: from config.settings import settings
 7: 
 8: def setup_logger(name: str, level: str = None) -> logger:
 9:     """
10:     Настройка логгера
11: 
12:     Args:
13:         name: Имя логгера
14:         level: Уровень логирования
15: 
16:     Returns:
17:         Настроенный логгер
18:     """
19:     # Удаляем стандартный handler
20:     logger.remove()
21: 
22:     # Добавляем новый handler с форматированием
23:     logger.add(
24:         sys.stdout,
25:         level=level or settings.LOG_LEVEL,
26:         format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
27:         colorize=True
28:     )
29: 
30:     # Добавляем handler для файлов (если нужно)
31:     # logger.add(
32:     #     "logs/antifraud.log",
33:     #     rotation="500 MB",
34:     #     level="INFO",
35:     #     format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
36:     # )
37: 
38:     return logger
````

## File: ai.md
````markdown
  1: # Микросервис оценки финансовых транзакций
  2: 
  3: ## Стек
  4: - Python 3.12+
  5: - FastAPI
  6: - Pydantic
  7: - Redis (кэш)
  8: - UoW (Unit of Work)
  9: - Repository Pattern
 10: - Dependency Injection
 11: - Loguru (/logging)
 12: - Async/await
 13: - Docker
 14: - Prometheus
 15: - Locust (для генерации трафика)
 16: 
 17: ## Архитектурный стиль
 18: - Service Layer Architecture
 19: - Dependency Injection (на уровне FastAPI)
 20: - Repository Pattern для работы с Redis
 21: - Clean Architecture с четким разделением ответственности
 22: - Микросервисная архитектура
 23: 
 24: ## Module Map
 25: - `main.py` - точка входа FastAPI приложения
 26: - `models/transaction.py` - Pydantic модели для транзакций
 27: - `models/scoring.py` - модели для результатов оценки
 28: - `services/transaction_service.py` - бизнес-логика обработки транзакций
 29: - `services/scoring_service.py` - сервис для работы с ML моделью
 30: - `repositories/transaction_repository.py` - репозиторий для работы с Redis
 31: - `utils/logger.py` - конфигурация логгирования
 32: - `config/settings.py` - настройки приложения
 33: - `api/routes/transaction.py` - REST API маршруты
 34: - `api/middleware/logging.py` - middleware для логирования
 35: - `exceptions/` - пользовательские исключения
 36: - `load_generator/traffic_generator.py` - генератор трафика
 37: - `monitoring/metrics.py` - модуль настройки метрик мониторинга
 38: - `tests/` - тесты проекта
 39: - `Dockerfile` - конфигурация Docker образа
 40: - `docker-compose.yaml` - docker-compose для основного сервиса
 41: - `docker-compose.traffic.yaml` - docker-compose для генератора трафика
 42: - `prometheus.yml` - конфигурация Prometheus
 43: 
 44: ## Public Interfaces
 45: 
 46: ### Models
 47: ```python
 48: # models/transaction.py
 49: from pydantic import BaseModel
 50: from typing import Optional
 51: 
 52: class Transaction(BaseModel):
 53:     customer_id: str
 54:     transaction_id: str
 55:     amount: float
 56:     type: int
 57:     currency: str
 58:     timestamp: str
 59:     merchant_id: str
 60:     card_bin: str
 61:     ip_address: str
 62:     device_id: str
 63:     location: str
 64:     channel: str
 65:     is_fraud: Optional[bool] = None
 66:     # ... остальные поля
 67: 
 68: # models/scoring.py
 69: from pydantic import BaseModel
 70: from typing import Optional
 71: 
 72: class ScoringResult(BaseModel):
 73:     transaction_id: str
 74:     scoring: float
 75:     is_fraud: Optional[bool] = None
 76:     # ... остальные поля
 77: ```
 78: 
 79: ### Repositories
 80: ```python
 81: # repositories/transaction_repository.py
 82: from abc import ABC, abstractmethod
 83: from typing import List
 84: from models.transaction import Transaction
 85: 
 86: class TransactionRepository(ABC):
 87:     @abstractmethod
 88:     async def add_transaction(self, transaction: Transaction) -> None:
 89:         ...
 90: 
 91:     @abstractmethod
 92:     async def get_transactions_by_customer(self, customer_id: str) -> List[Transaction]:
 93:         ...
 94: 
 95:     @abstractmethod
 96:     async def get_statistics_by_customer(self, customer_id: str) -> dict:
 97:         ...
 98: 
 99:     @abstractmethod
100:     async def update_statistics(self, customer_id: str, stats: dict) -> None:
101:         ...
102: 
103:     @abstractmethod
104:     async def get_cached_transaction(self, customer_id: str) -> Transaction:
105:         ...
106: 
107:     @abstractmethod
108:     async def delete_expired_transactions(self) -> None:
109:         ...
110: ```
111: 
112: ### Services
113: ```python
114: # services/transaction_service.py
115: from models.transaction import Transaction
116: from models.scoring import ScoringResult
117: from repositories.transaction_repository import TransactionRepository
118: 
119: class TransactionService:
120:     async def process_transaction(self, transaction: Transaction) -> ScoringResult:
121:         ...
122: 
123: # services/scoring_service.py
124: from models.transaction import Transaction
125: from models.scoring import ScoringResult
126: 
127: class ScoringService:
128:     async def score_transaction(self, transaction: Transaction) -> ScoringResult:
129:         ...
130: ```
131: 
132: ### API Routes
133: ```python
134: # api/routes/transaction.py
135: from fastapi import APIRouter
136: from models.transaction import Transaction
137: from models.scoring import ScoringResult
138: 
139: router = APIRouter()
140: 
141: @router.post("/transactions", response_model=ScoringResult)
142: async def process_transaction(transaction: Transaction):
143:     ...
144: ```
145: 
146: ## Пример pyproject.toml
147: ```toml
148: [build-system]
149: requires = ["setuptools", "wheel"]
150: 
151: [project]
152: name = "antifraud-scoring-service"
153: version = "0.1.0"
154: description = "Microservice for financial transaction scoring"
155: authors = [{name = "Senior Python Architect"}]
156: license = "MIT"
157: readme = "README.md"
158: 
159: [project.dependencies]
160: fastapi = "^0.115.0"
161: pydantic = "^2.8.0"
162: redis = "^5.0.1"
163: loguru = "^0.7.2"
164: uvicorn = "^0.30.0"
165: asyncio = "^3.4.3"
166: typing-extensions = "^4.12.0"
167: prometheus-client = "^0.20.1"
168: prometheus-fastapi-instrumentator = "^7.0.0"
169: 
170: [project.optional-dependencies]
171: dev = [
172:     "pytest = ^8.3.0",
173:     "pytest-asyncio = ^0.23.0",
174:     "black = ^24.4.0",
175:     "flake8 = ^7.0.0",
176:     "locust = ^2.29.0",
177: ]
178: 
179: [project.scripts]
180: run-server = "main:main"
181: 
182: [tool.setuptools.packages.find]
183: where = ["."]
184: include = ["antifraud*"]
185: ```
````

## File: ARCHITECTURE.md
````markdown
  1: # Архитектура микросервиса оценки финансовых транзакций
  2: 
  3: ## Общая архитектура
  4: 
  5: Система построена по следующим принципам:
  6: 
  7: 1. **Service Layer Architecture** - Четкое разделение бизнес-логики
  8: 2. **Repository Pattern** - Абстракция работы с данными (в данном случае Redis)
  9: 3. **Dependency Injection** - Внедрение зависимостей через FastAPI
 10: 4. **Clean Architecture** - Четкое разделение слоев: API, Service, Repository, Models
 11: 5. **Микросервисная архитектура** - Система спроектирована как отдельный микросервис
 12: 
 13: ## Структура слоев
 14: 
 15: ### 1. API Layer (Представление)
 16: - **Файлы**: `api/routes/transaction.py`
 17: - **Ответственность**: Обработка HTTP запросов, маршрутизация, валидация входных данных
 18: - **Входные данные**: JSON с данными транзакции
 19: - **Выходные данные**: JSON с результатом оценки
 20: 
 21: ### 2. Service Layer (Бизнес логика)
 22: - **Файлы**: `services/transaction_service.py`, `services/scoring_service.py`
 23: - **Ответственность**:
 24:   - Обработка логики транзакции
 25:   - Вызов ML модели для оценки
 26:   - Расчет статистики по клиенту
 27:   - Обработка ошибок и таймаутов
 28: - **Связи**: Зависит от Repository для работы с данными
 29: 
 30: ### 3. Repository Layer (Доступ к данным)
 31: - **Файлы**: `repositories/transaction_repository.py`
 32: - **Ответственность**:
 33:   - Интерфейс для работы с Redis кэшем
 34:   - Добавление/извлечение транзакций
 35:   - Расчет статистики
 36: - **Реализация**: Конкретная реализация будет в `repositories/redis_transaction_repository.py`
 37: 
 38: ### 4. Model Layer (Модели данных)
 39: - **Файлы**: `models/transaction.py`, `models/scoring.py`
 40: - **Ответственность**:
 41:   - Определение структуры данных
 42:   - Валидация входных и выходных данных
 43:   - JSON схемы для API
 44: 
 45: ### 5. Utilities/Support Layer
 46: - **Файлы**: `utils/logger.py`, `api/middleware/logging.py`
 47: - **Ответственность**:
 48:   - Логгирование запросов
 49:   - Middleware для обработки запросов
 50: 
 51: ### 6. Monitoring Layer (Мониторинг)
 52: - **Файлы**: `monitoring/metrics.py`
 53: - **Ответственность**:
 54:   - Настройка метрик Prometheus
 55:   - Экспорт метрик для системы мониторинга
 56: 
 57: ### 7. Load Generation Layer (Генератор трафика)
 58: - **Файлы**: `load_generator/traffic_generator.py`
 59: - **Ответственность**:
 60:   - Генерация нагрузки для тестирования
 61:   - Симуляция транзакций с различными параметрами
 62:   - Отслеживание статистики обработки
 63: 
 64: ## Путь запроса (Request Flow)
 65: 
 66: ### 1. Входящий запрос
 67: Клиент отправляет POST запрос на `/api/v1/transactions` с JSON телом:
 68: 
 69: ```json
 70: {
 71:   "customer_id": "customer_123",
 72:   "transaction_id": "txn_456",
 73:   "amount": 100.50,
 74:   "currency": "USD",
 75:   "type": 78,
 76:   "merchant_id": "merchant_789",
 77:   "card_bin": "411111",
 78:   "ip_address": "192.168.1.1",
 79:   "device_id": "device_001",
 80:   "location": "US-NY",
 81:   "channel": "online",
 82:   "timestamp": "2023-01-01T10:00:00Z"
 83: }
 84: ```
 85: 
 86: ### 2. API обработчик
 87: - **Файл**: `api/routes/transaction.py`
 88: - **Действие**: Принимает запрос, валидирует данные с помощью Pydantic модели `Transaction`
 89: - **Логирование**: Записывает информацию о входящем запросе в логи
 90: - **Передача**: Передает данные в `TransactionService`
 91: 
 92: ### 3. Service Layer (Обработка транзакции)
 93: - **Файл**: `services/transaction_service.py`
 94: - **Действие**:
 95:   - Валидация транзакции
 96:   - Замер времени начала обработки
 97:   - Добавление транзакции в кэш (Redis)
 98:   - Получение истории транзакций по клиенту
 99:   - Расчет статистики для клиента
100:   - Вызов Scoring Service
101: 
102: ### 4. Repository Layer (Работа с кэшем)
103: - **Файл**: `repositories/transaction_repository.py`
104: - **Действие**:
105:   - Добавление транзакции в Redis с TTL 24 часа
106:   - Получение всех транзакций по customer_id
107:   - Изменение счетчиков и статистики
108:   - Обновление вспомогательных данных для расчета средних значений
109: 
110: ### 5. Scoring Service (Оценка с ML)
111: - **Файл**: `services/scoring_service.py`
112: - **Действие**:
113:   - Вызов ML модели для оценки транзакции
114:   - Если модель не отвечает вовремя - возвращается значение по умолчанию
115:   - Возврат результата оценки
116: 
117: ### 6. Формирование ответа
118: - **Файл**: `services/transaction_service.py`
119: - **Действие**:
120:   - Формирование полного ответа с результатом оценки
121:   - Расчет времени обработки (должно быть <= 100-200ms)
122:   - Добавление всех необходимых статистических данных
123:   - Запись в логи о завершении обработки
124: 
125: ### 7. Возвращение ответа
126: - **Файл**: `api/routes/transaction.py`
127: - **Действие**:
128:   - Формирование JSON ответа по модели `ScoringResult`
129:   - Отправка HTTP ответа клиенту с кодом 200
130:   - Запись в логи о завершении запроса и времени обработки
131: 
132: ## Схема взаимодействия
133: 
134: ```
135: [Клиент]
136:     ↓
137: [API Layer] → [Service Layer] → [Repository Layer] → [Redis]
138:     ↑                              ↓
139:     |                      [Scoring Service]
140:     |                              ↓
141:     |                      [ML Model (заглушка)]
142:     |                              ↓
143:     ↓                        [Возврат результата]
144: [Ответ JSON]
145: ```
146: 
147: ## Требования к производительности
148: 
149: 1. **Время обработки**: Не более 200мс
150: 2. **Максимальное время оценки**: 100мс для ML модели
151: 3. **Таймаут по умолчанию**: Если ML модель не отвечает, возвращать значение по умолчанию (0.5)
152: 4. **Кэш**: 24 часа жизни записей, автоматическое удаление истекших
153: 
154: ## Логгирование
155: 
156: Все действия логгируются с использованием Loguru:
157: - Входящие запросы с ID транзакции
158: - Завершение обработки запроса с временем выполнения
159: - Ошибки обработки
160: - Системные события (запуск/остановка сервиса)
161: 
162: ## Ошибки и обработка
163: 
164: 1. **Валидация данных**: Происходит на уровне Pydantic
165: 2. **Ошибки сервиса**: Возвращаются как HTTP 500
166: 3. **Таймауты**: Специальная обработка через `ModelTimeoutError`
167: 4. **Кэш ошибки**: Обработка ошибок Redis через `CacheError`
168: 
169: ## Мониторинг и метрики
170: 
171: Система поддерживает комплексную систему мониторинга:
172: 
173: 1. **Prometheus Metrics**:
174:    - Счетчики запросов по методам и эндпоинтам
175:    - Гистограммы времени обработки запросов
176:    - Gauge для отслеживания активных запросов
177: 
178: 2. **Мониторинг Redis**:
179:    - Использование Redis Exporter для экспорта метрик Redis в Prometheus
180:    - Отслеживание состояния кэша и производительности
181: 
182: 3. **Визуализация**:
183:    - Grafana для визуализации метрик
184:    - Конфигурация для настройки dashboards
185: 
186: 4. **Логирование**:
187:    - Использование Loguru для детального логирования
188:    - Логи доступны для анализа в системы типа OpenSearch
189: 
190: ## Генератор трафика
191: 
192: Для тестирования производительности и функциональности системы используется генератор трафика:
193: 
194: 1. **Features**:
195:    - Асинхронная генерация транзакций с использованием aiohttp
196:    - Генерация случайных данных для транзакций
197:    - Настройка количества транзакций в секунду
198:    - Отслеживание статистики (успешные/ошибочные запросы)
199:    - Интеграция с мониторингом
200: 
201: 2. **Конфигурация**:
202:    - Максимальное количество транзакций в секунду (по умолчанию 1000)
203:    - Возможность настройки URL сервиса
204:    - Поддержка различий в типах транзакций, валютах, каналах и т.д.
205: 
206: 3. **Тестирование**:
207:    - Позволяет проверить производительность сервиса под нагрузкой
208:    - Отслеживает задержки и отказы
209:    - Используется для нагрузочного тестирования
````

## File: docker-compose.traffic.yaml
````yaml
 1: version: '3.8'
 2: 
 3: services:
 4:   traffic-generator:
 5:     build: .
 6:     container_name: antifraud-traffic-generator
 7:     command: python -m load_generator.traffic_generator
 8:     environment:
 9:       - BASE_URL=http://antifraud-service:8000
10:       - MAX_TRANSACTIONS=1000
11:     depends_on:
12:       - antifraud-service
13:     networks:
14:       - antifraud-network
15: 
16:   antifraud-service:
17:     image: antifraud-service
18:     container_name: antifraud-service
19:     ports:
20:       - "8000:8000"
21:     environment:
22:       - REDIS_HOST=redis
23:       - REDIS_PORT=6379
24:       - LOG_LEVEL=INFO
25:     depends_on:
26:       - redis
27:     networks:
28:       - antifraud-network
29: 
30:   redis:
31:     image: redis:7-alpine
32:     container_name: antifraud-redis
33:     ports:
34:       - "6379:6379"
35:     volumes:
36:       - redis_data:/data
37:     networks:
38:       - antifraud-network
39: 
40: volumes:
41:   redis_data:
42: 
43: networks:
44:   antifraud-network:
45:     driver: bridge
````

## File: docker-compose.yaml
````yaml
 1: version: '3.8'
 2: 
 3: services:
 4:   antifraud-service:
 5:     build: .
 6:     container_name: antifraud-service
 7:     ports:
 8:       - "8000:8000"
 9:     environment:
10:       - REDIS_HOST=redis
11:       - REDIS_PORT=6379
12:       - LOG_LEVEL=INFO
13:     depends_on:
14:       - redis
15:     networks:
16:       - antifraud-network
17: 
18:   redis:
19:     image: redis:7-alpine
20:     container_name: antifraud-redis
21:     ports:
22:       - "6379:6379"
23:     volumes:
24:       - redis_data:/data
25:     networks:
26:       - antifraud-network
27: 
28:   # Prometheus для мониторинга
29:   prometheus:
30:     image: prom/prometheus:latest
31:     container_name: antifraud-prometheus
32:     ports:
33:       - "9090:9090"
34:     volumes:
35:       - ./prometheus.yml:/etc/prometheus/prometheus.yml
36:     networks:
37:       - antifraud-network
38: 
39:   # Redis Exporter
40:   redis-exporter:
41:     image: oliver006/redis_exporter:latest
42:     container_name: antifraud-redis-exporter
43:     ports:
44:       - "9121:9121"
45:     environment:
46:       REDIS_ADDR: redis://redis:6379
47:     depends_on:
48:       - redis
49:     networks:
50:       - antifraud-network
51: 
52:   # Grafana для визуализации метрик
53:   grafana:
54:     image: grafana/grafana:latest
55:     container_name: antifraud-grafana
56:     ports:
57:       - "3000:3000"
58:     depends_on:
59:       - prometheus
60:     networks:
61:       - antifraud-network
62: 
63: volumes:
64:   redis_data:
65: 
66: networks:
67:   antifraud-network:
68:     driver: bridge
````

## File: Dockerfile
````dockerfile
 1: FROM python:3.12-slim
 2: 
 3: # Установка зависимостей
 4: RUN apt-get update && apt-get install -y \
 5:     gcc \
 6:     && rm -rf /var/lib/apt/lists/*
 7: 
 8: # Установка рабочей директории
 9: WORKDIR /app
10: 
11: # Копирование файлов зависимостей
12: COPY pyproject.toml .
13: 
14: # Установка зависимостей Python
15: RUN pip install --no-cache-dir .
16: 
17: # Копирование всего кода
18: COPY . .
19: 
20: # Экспозиция порта
21: EXPOSE 8000
22: 
23: # Команда запуска
24: CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
````

## File: main.py
````python
 1: """
 2: Микросервис оценки финансовых транзакций
 3: """
 4: import asyncio
 5: import logging
 6: from fastapi import FastAPI
 7: from fastapi.middleware.logging import LoggingMiddleware
 8: from prometheus_fastapi_instrumentator import Instrumentator
 9: from api.routes.transaction import router as transaction_router
10: from config.settings import settings
11: from utils.logger import setup_logger
12: from monitoring.metrics import setup_metrics
13: 
14: # Инициализация логгера
15: logger = setup_logger(__name__)
16: 
17: # Создание экземпляра приложения FastAPI
18: app = FastAPI(
19:     title="Antifraud Scoring Service",
20:     description="Микросервис для оценки финансовых транзакций",
21:     version="0.1.0"
22: )
23: 
24: # Настройка инструментов мониторинга
25: setup_metrics(app)
26: 
27: # Добавление middleware для логирования
28: app.add_middleware(LoggingMiddleware)
29: 
30: # Регистрация маршрутов
31: app.include_router(transaction_router, prefix="/api/v1")
32: 
33: @app.on_event("startup")
34: async def startup_event():
35:     """Событие запуска приложения"""
36:     logger.info("Запуск микросервиса оценки транзакций")
37:     # Здесь можно инициализировать соединения с базами данных, кэшами и т.д.
38:     pass
39: 
40: @app.on_event("shutdown")
41: async def shutdown_event():
42:     """Событие остановки приложения"""
43:     logger.info("Остановка микросервиса оценки транзакций")
44:     # Здесь можно закрывать соединения, очищать ресурсы и т.д.
45:     pass
46: 
47: @app.get("/")
48: async def root():
49:     """Корневой эндпоинт"""
50:     return {"message": "Микросервис оценки финансовых транзакций запущен"}
51: 
52: @app.get("/health")
53: async def health_check():
54:     """Проверка состояния сервиса"""
55:     return {"status": "healthy"}
56: 
57: @app.get("/metrics")
58: async def metrics():
59:     """Эндпоинт метрик Prometheus"""
60:     from prometheus_client import generate_latest
61:     return generate_latest()
62: 
63: if __name__ == "__main__":
64:     import uvicorn
65:     uvicorn.run(app, host="0.0.0.0", port=8000)
````

## File: prometheus.yml
````yaml
 1: global:
 2:   scrape_interval: 15s
 3: 
 4: scrape_configs:
 5:   - job_name: 'antifraud-service'
 6:     static_configs:
 7:       - targets: ['antifraud-service:8000']
 8: 
 9:   - job_name: 'redis-exporter'
10:     static_configs:
11:       - targets: ['redis-exporter:9121']
````

## File: pyproject.toml
````toml
 1: [build-system]
 2: requires = ["setuptools", "wheel"]
 3: 
 4: [project]
 5: name = "antifraud-scoring-service"
 6: version = "0.1.0"
 7: description = "Microservice for financial transaction scoring"
 8: authors = [{name = "Senior Python Architect"}]
 9: license = "MIT"
10: readme = "README.md"
11: 
12: [project.dependencies]
13: fastapi = "^0.115.0"
14: pydantic = "^2.8.0"
15: redis = "^5.0.1"
16: loguru = "^0.7.2"
17: uvicorn = "^0.30.0"
18: asyncio = "^3.4.3"
19: typing-extensions = "^4.12.0"
20: prometheus-client = "^0.20.1"
21: prometheus-fastapi-instrumentator = "^7.0.0"
22: 
23: [project.optional-dependencies]
24: dev = [
25:     "pytest = ^8.3.0",
26:     "pytest-asyncio = ^0.23.0",
27:     "black = ^24.4.0",
28:     "flake8 = ^7.0.0",
29:     "locust = ^2.29.0",
30: ]
31: 
32: [project.scripts]
33: run-server = "main:main"
34: 
35: [tool.setuptools.packages.find]
36: where = ["."]
37: include = ["antifraud*"]
````
