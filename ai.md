# Микросервис оценки финансовых транзакций

## Стек
- Python 3.12+
- FastAPI
- Pydantic v2
- Redis (кэш) с async redis.asyncio
- Repository Pattern
- Dependency Injection
- Loguru (логгирование)
- Async/await
- Docker
- Prometheus
- aiohttp (генератор трафика)

## Архитектурный стиль
- Service Layer Architecture
- Dependency Injection (на уровне FastAPI через app state)
- Repository Pattern для работы с Redis
- Clean Architecture с четким разделением ответственности
- Микросервисная архитектура

## Module Map
- `main.py` - точка входа FastAPI приложения, DI провайдеры
- `models/transaction.py` - Pydantic модели для транзакций
- `models/scoring.py` - модели для результатов оценки
- `services/transaction_service.py` - ABC интерфейс сервиса транзакций
- `services/transaction_service_impl.py` - реализация сервиса транзакций
- `services/scoring_service.py` - ABC интерфейс ML сервиса
- `services/scoring_service_impl.py` - реализация ML сервиса
- `repositories/transaction_repository.py` - ABC интерфейс репозитория
- `repositories/redis_transaction_repository.py` - реализация с async redis.asyncio
- `utils/logger.py` - конфигурация логгирования
- `config/settings.py` - настройки приложения
- `api/routes/transaction.py` - REST API маршруты
- `api/middleware/logging.py` - middleware для логирования
- `exceptions/` - пользовательские исключения
- `load_generator/traffic_generator.py` - генератор трафика (aiohttp)
- `monitoring/metrics.py` - модуль настройки метрик мониторинга
- `tests/` - тесты проекта
- `Dockerfile` - конфигурация Docker образа
- `docker-compose.yaml` - docker-compose для основного сервиса
- `docker-compose.traffic.yaml` - docker-compose для генератора трафика
- `prometheus.yml` - конфигурация Prometheus

## Public Interfaces

### Models
```python
# models/transaction.py
from pydantic import BaseModel
from typing import Optional

class Transaction(BaseModel):
    customer_id: str
    transaction_id: str
    amount: float
    type: int
    currency: str
    timestamp: str
    merchant_id: str
    card_bin: str
    ip_address: str
    device_id: str
    location: str
    channel: str
    is_fraud: Optional[bool] = None
    # ... остальные поля

# models/scoring.py
from pydantic import BaseModel
from typing import Optional

class ScoringResult(BaseModel):
    transaction_id: str
    scoring: float
    is_fraud: Optional[bool] = None
    # ... остальные поля
```

### Repositories
```python
# repositories/transaction_repository.py (ABC)
from abc import ABC, abstractmethod
from typing import List
from models.transaction import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    async def add_transaction(self, transaction: Transaction) -> None: ...
    @abstractmethod
    async def get_transactions_by_customer(self, customer_id: str) -> List[Transaction]: ...
    @abstractmethod
    async def get_statistics_by_customer(self, customer_id: str) -> dict: ...
    @abstractmethod
    async def update_statistics(self, customer_id: str, stats: dict) -> None: ...
    @abstractmethod
    async def get_cached_transaction(self, customer_id: str) -> Transaction: ...
    @abstractmethod
    async def delete_expired_transactions(self) -> None: ...

# repositories/redis_transaction_repository.py (Реализация)
from redis.asyncio import ConnectionPool
import redis.asyncio as redis

class RedisTransactionRepository(TransactionRepository):
    def __init__(self, host, port, db, password=None):
        self._pool = ConnectionPool(
            host=host, port=port, db=db,
            max_connections=50, decode_responses=True
        )
        self._client = redis.Redis(connection_pool=self._pool)
```

### Services
```python
# services/transaction_service.py (ABC)
from abc import ABC, abstractmethod
from models.transaction import Transaction
from models.scoring import ScoringResult

class TransactionService(ABC):
    @abstractmethod
    async def process_transaction(self, transaction: Transaction) -> ScoringResult: ...

# services/transaction_service_impl.py (Реализация)
class TransactionServiceImpl(TransactionService):
    def __init__(self, repository, scoring_service):
        self._repository = repository
        self._scoring_service = scoring_service
```

### API Routes
```python
# api/routes/transaction.py
from fastapi import APIRouter
from models.transaction import Transaction
from models.scoring import ScoringResult

router = APIRouter(prefix="/transactions")

@router.post("/", response_model=ScoringResult)
async def process_transaction(transaction: Transaction):
    from main import get_transaction_service
    service = get_transaction_service()
    return await service.process_transaction(transaction)
```

## Пример pyproject.toml
```toml
[build-system]
requires = ["setuptools", "wheel"]

[project]
name = "antifraud-scoring-service"
version = "0.1.0"
description = "Microservice for financial transaction scoring"
authors = [{name = "Senior Python Architect"}]
license = "MIT"
readme = "README.md"

[project.dependencies]
fastapi = "^0.115.0"
pydantic = "^2.8.0"
redis = {version = "^5.0.1", extras = ["asyncio"]}
loguru = "^0.7.2"
uvicorn = {version = "^0.30.0", extras = ["standard"]}
typing-extensions = "^4.12.0"
prometheus-client = "^0.20.1"
prometheus-fastapi-instrumentator = "^7.0.0"

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.23.0",
    "black>=24.4.0",
    "flake8>=7.0.0",
    "locust>=2.29.0",
]

[project.scripts]
run-server = "main:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["antifraud*"]
```