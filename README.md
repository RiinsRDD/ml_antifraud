# Микросервис оценки финансовых транзакций

## Описание

Микросервис для оценки финансовых транзакций с использованием машинного обучения. Сервис принимает транзакции, добавляет их в кэш Redis, рассчитывает статистику по клиенту и возвращает оценку риска.

## Архитектура

Система построена по принципам Service Layer Architecture и Clean Architecture с четким разделением ответственности:

1. **API Layer** - обработка HTTP запросов и маршрутизация
2. **Service Layer** - бизнес-логика обработки транзакций и взаимодействия с ML моделью
3. **Repository Layer** - работа с Redis кэшем
4. **Model Layer** - модели данных с валидацией
5. **Monitoring Layer** - система мониторинга и метрик

## Стек технологий

- Python 3.12+
- FastAPI
- Pydantic
- Redis (кэш)
- Prometheus & Grafana (мониторинг)
- Docker (контейнеризация)
- Locust (генератор трафика)
- Loguru (логирование)

## Структура проекта

```
.
├── main.py                  # Точка входа сервиса
├── ai.md                    # Архитектурная документация
├── ARCHITECTURE.md          # Детальное описание архитектуры
├── .gitignore               # Файл игнорирования файлов git
├── Dockerfile               # Конфигурация Docker образа
├── docker-compose.yaml      # Docker compose для основного сервиса
├── docker-compose.traffic.yaml # Docker compose для генератора трафика
├── prometheus.yml           # Конфигурация Prometheus
├── pyproject.toml           # Файл зависимостей проекта
├── models/                  # Модели данных
│   ├── transaction.py       # Модель транзакции
│   └── scoring.py           # Модель результата оценки
├── services/                # Бизнес-логика
│   ├── transaction_service.py  # Сервис обработки транзакций
│   └── scoring_service.py   # Сервис оценки
├── repositories/            # Репозитории данных
│   └── transaction_repository.py  # Интерфейс работы с Redis
├── api/                     # API маршруты
│   ├── routes/              # Маршруты
│   │   └── transaction.py   # Маршрут для транзакций
│   └── middleware/          # Middleware
│       └── logging.py       # Middleware для логирования
├── utils/                   # Вспомогательные модули
│   └── logger.py            # Конфигурация логгирования
├── config/                  # Конфигурация
│   └── settings.py          # Настройки приложения
├── load_generator/          # Генератор трафика
│   └── traffic_generator.py # Модуль генерации нагрузки
├── monitoring/              # Модули мониторинга
│   └── metrics.py           # Метрики Prometheus
├── tests/                   # Тесты
└── requirements.txt         # Файл зависимостей (если нужен)
```

## Запуск сервиса

### Локальный запуск

1. Установите зависимости:
```bash
pip install -e .
```

2. Запустите Redis (можно через Docker):
```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

3. Запустите сервис:
```bash
python main.py
```

### Запуск через Docker

1. Сборка и запуск:
```bash
docker-compose up --build
```

2. Сервис будет доступен по адресу: http://localhost:8000

### Запуск генератора трафика

```bash
docker-compose -f docker-compose.traffic.yaml up --build
```

## Мониторинг

Система поддерживает мониторинг через Prometheus и Grafana:

1. **Metrics endpoint**: http://localhost:8000/metrics
2. **Prometheus**: http://localhost:9090
3. **Grafana**: http://localhost:3000 (логин/пароль по умолчанию: admin/admin)

## API

### Запросы

- `POST /api/v1/transactions` - Обработка транзакции
  - Тело запроса: JSON с данными транзакции
  - Ответ: JSON с результатом оценки

### Пример запроса

```json
{
  "customer_id": "customer_123",
  "transaction_id": "txn_456",
  "amount": 100.50,
  "currency": "USD",
  "type": 78,
  "merchant_id": "merchant_789",
  "card_bin": "411111",
  "ip_address": "192.168.1.1",
  "device_id": "device_001",
  "location": "US-NY",
  "channel": "online",
  "timestamp": "2023-01-01T10:00:00Z"
}
```

### Пример ответа

```json
{
  "customer_id": "customer_123",
  "transaction_id": "txn_456",
  "scoring": 0.25,
  "is_fraud": false,
  "processing_time_ms": 85,
  "customer_transaction_count_24h": 15,
  "customer_avg_amount_24h": 75.25,
  "customer_transaction_count_3h": 2,
  "customer_avg_amount_3h": 100.0,
  "customer_transaction_count_6h": 5,
  "customer_avg_amount_6h": 90.5,
  "customer_transaction_count_12h": 8,
  "customer_avg_amount_12h": 85.75,
  "processed_at": "2023-01-01T10:00:00Z"
}
```

## Требования к производительности

- Время обработки запросов: не более 200мс
- Максимальное время оценки ML модели: 100мс
- Таймаут по умолчанию при ошибке: 0.5

## Разработка

1. Установка зависимостей для разработки:
```bash
pip install -e ".[dev]"
```

2. Запуск тестов:
```bash
pytest tests/
```

3. Форматирование кода:
```bash
black .
```

## Безопасность

Система реализует следующие меры безопасности:

- Валидация входных данных через Pydantic
- Логирование всех запросов и ошибок
- Использование HTTPS при необходимости
- Правильная обработка ошибок и таймаутов

## Поддержка и обновления

Для получения помощи или обращения по вопросам:
- Создайте issue в репозитории
- Следите за обновлениями в GitHub