# Микросервис оценки финансовых транзакций

## Стек
- Python 3.12+
- FastAPI
- Pydantic
- Redis (кэш)
- UoW (Unit of Work)
- Repository Pattern
- Dependency Injection
- Loguru (/logging)
- Async/await
- Docker
- Prometheus
- Locust (для генерации трафика)

## Архитектурный стиль
- Service Layer Architecture
- Dependency Injection (на уровне FastAPI)
- Repository Pattern для работы с Redis
- Clean Architecture с четким разделением ответственности
- Микросервисная архитектура

## Module Map
- `main.py` - точка входа FastAPI приложения
- `models/transaction.py` - Pydantic модели для транзакций
- `models/scoring.py` - модели для результатов оценки
- `services/transaction_service.py` - бизнес-логика обработки транзакций
- `services/scoring_service.py` - сервис для работы с ML моделью
- `repositories/transaction_repository.py` - репозиторий для работы с Redis
- `utils/logger.py` - конфигурация логгирования
- `config/settings.py` - настройки приложения
- `api/routes/transaction.py` - REST API маршруты
- `api/middleware/logging.py` - middleware для логирования
- `exceptions/` - пользовательские исключения
- `load_generator/traffic_generator.py` - генератор трафика
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
# repositories/transaction_repository.py
from abc import ABC, abstractmethod
from typing import List
from models.transaction import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    async def add_transaction(self, transaction: Transaction) -> None:
        ...

    @abstractmethod
    async def get_transactions_by_customer(self, customer_id: str) -> List[Transaction]:
        ...

    @abstractmethod
    async def get_statistics_by_customer(self, customer_id: str) -> dict:
        ...

    @abstractmethod
    async def update_statistics(self, customer_id: str, stats: dict) -> None:
        ...

    @abstractmethod
    async def get_cached_transaction(self, customer_id: str) -> Transaction:
        ...

    @abstractmethod
    async def delete_expired_transactions(self) -> None:
        ...
```

### Services
```python
# services/transaction_service.py
from models.transaction import Transaction
from models.scoring import ScoringResult
from repositories.transaction_repository import TransactionRepository

class TransactionService:
    async def process_transaction(self, transaction: Transaction) -> ScoringResult:
        ...

# services/scoring_service.py
from models.transaction import Transaction
from models.scoring import ScoringResult

class ScoringService:
    async def score_transaction(self, transaction: Transaction) -> ScoringResult:
        ...
```

### API Routes
```python
# api/routes/transaction.py
from fastapi import APIRouter
from models.transaction import Transaction
from models.scoring import ScoringResult

router = APIRouter()

@router.post("/transactions", response_model=ScoringResult)
async def process_transaction(transaction: Transaction):
    ...
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
redis = "^5.0.1"
loguru = "^0.7.2"
uvicorn = "^0.30.0"
asyncio = "^3.4.3"
typing-extensions = "^4.12.0"
prometheus-client = "^0.20.1"
prometheus-fastapi-instrumentator = "^7.0.0"

[project.optional-dependencies]
dev = [
    "pytest = ^8.3.0",
    "pytest-asyncio = ^0.23.0",
    "black = ^24.4.0",
    "flake8 = ^7.0.0",
    "locust = ^2.29.0",
]

[project.scripts]
run-server = "main:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["antifraud*"]
```