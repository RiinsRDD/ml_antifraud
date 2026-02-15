"""
Модели результатов оценки
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ScoringResult(BaseModel):
    """Результат оценки транзакции"""

    # Обязательные поля из входной транзакции
    customer_id: str = Field(..., description="ID клиента")
    transaction_id: str = Field(..., description="ID транзакции")

    # Поле оценки
    scoring: float = Field(..., description="Оценка риска транзакции от 0 до 1")

    # Дополнительные поля для анализа
    is_fraud: Optional[bool] = Field(None, description="Флаг мошенничества (по оценке)")
    processing_time_ms: Optional[int] = Field(None, description="Время обработки в миллисекундах")

    # Статистика по клиенту
    customer_transaction_count_24h: Optional[int] = Field(None, description="Количество транзакций за 24 часа")
    customer_avg_amount_24h: Optional[float] = Field(None, description="Средняя сумма за 24 часа")
    customer_transaction_count_3h: Optional[int] = Field(None, description="Количество транзакций за 3 часа")
    customer_avg_amount_3h: Optional[float] = Field(None, description="Средняя сумма за 3 часа")
    customer_transaction_count_6h: Optional[int] = Field(None, description="Количество транзакций за 6 часов")
    customer_avg_amount_6h: Optional[float] = Field(None, description="Средняя сумма за 6 часов")
    customer_transaction_count_12h: Optional[int] = Field(None, description="Количество транзакций за 12 часов")
    customer_avg_amount_12h: Optional[float] = Field(None, description="Средняя сумма за 12 часов")

    # Временные метки
    processed_at: str = Field(..., description="Время обработки")

    class Config:
        """Конфигурация модели"""
        schema_extra = {
            "example": {
                "customer_id": "customer_123",
                "transaction_id": "txn_456",
                "scoring": 0.25,
                "is_fraud": False,
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
        }