"""
Модели транзакций
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Transaction(BaseModel):
    """Модель финансовой транзакции"""

    # Обязательные поля
    customer_id: str = Field(..., description="ID клиента")
    transaction_id: str = Field(..., description="ID транзакции")

    # Основные финансовые данные
    amount: float = Field(..., description="Сумма транзакции")
    currency: str = Field(..., description="Валюта транзакции")
    type: int = Field(..., description="Тип транзакции")

    # Дополнительные поля для анализа
    merchant_id: str = Field(..., description="ID мерчанта")
    card_bin: str = Field(..., description="BIN номер карты")
    ip_address: str = Field(..., description="IP адрес клиента")
    device_id: str = Field(..., description="ID устройства")
    location: str = Field(..., description="Местоположение")
    channel: str = Field(..., description="Канал транзакции")

    # Временные метки
    timestamp: str = Field(..., description="Временная метка транзакции")

    # Поля для анализа
    is_fraud: Optional[bool] = Field(None, description="Флаг мошенничества")
    merchant_risk_score: Optional[float] = Field(None, description="Рейтинг риска мерчанта")
    card_risk_score: Optional[float] = Field(None, description="Рейтинг риска карты")
    customer_risk_score: Optional[float] = Field(None, description="Рейтинг риска клиента")

    # Дополнительные поля
    is_velocity_alert: Optional[bool] = Field(None, description="Оповещение о скорости транзакций")
    is_location_alert: Optional[bool] = Field(None, description="Оповещение о геолокации")
    is_device_alert: Optional[bool] = Field(None, description="Оповещение об устройстве")

    # Поля для будущего использования
    customer_segments: Optional[List[str]] = Field(None, description="Сегменты клиента")
    transaction_category: Optional[str] = Field(None, description="Категория транзакции")
    is_high_value: Optional[bool] = Field(None, description="Высокая стоимость транзакции")

    class Config:
        """Конфигурация модели"""
        schema_extra = {
            "example": {
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
                "timestamp": "2023-01-01T10:00:00Z",
                "is_fraud": False,
                "merchant_risk_score": 0.2,
                "card_risk_score": 0.1,
                "customer_risk_score": 0.3,
            }
        }