"""
Тесты для моделей данных
"""
import pytest
from models.transaction import Transaction
from models.scoring import ScoringResult


def test_transaction_model_valid():
    """Тест валидации модели транзакции"""
    transaction_data = {
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

    transaction = Transaction(**transaction_data)

    assert transaction.customer_id == "customer_123"
    assert transaction.transaction_id == "txn_456"
    assert transaction.amount == 100.50
    assert transaction.currency == "USD"
    assert transaction.type == 78
    assert transaction.timestamp == "2023-01-01T10:00:00Z"


def test_transaction_model_invalid():
    """Тест валидации модели транзакции с неверными данными"""
    transaction_data = {
        "customer_id": "customer_123",
        "amount": 100.50,  # отсутствует обязательное поле transaction_id
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

    with pytest.raises(Exception):  # Pydantic генерирует исключение при невалидных данных
        Transaction(**transaction_data)


def test_scoring_result_model():
    """Тест модели результата оценки"""
    scoring_data = {
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

    scoring_result = ScoringResult(**scoring_data)

    assert scoring_result.customer_id == "customer_123"
    assert scoring_result.transaction_id == "txn_456"
    assert scoring_result.scoring == 0.25
    assert scoring_result.is_fraud is False
    assert scoring_result.processing_time_ms == 85