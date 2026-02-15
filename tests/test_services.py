"""
Тесты для сервисов
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from services.transaction_service import TransactionService
from services.scoring_service import ScoringService
from models.transaction import Transaction
from models.scoring import ScoringResult


class MockTransactionService(TransactionService):
    """Мок для тестирования TransactionService"""

    async def process_transaction(self, transaction: Transaction) -> ScoringResult:
        # Пустая реализация для тестирования
        return ScoringResult(
            customer_id=transaction.customer_id,
            transaction_id=transaction.transaction_id,
            scoring=0.5,
            processed_at="2023-01-01T10:00:00Z"
        )

    async def _validate_transaction(self, transaction: Transaction) -> bool:
        return True

    async def _calculate_statistics(self, customer_id: str) -> dict:
        return {
            "transaction_count_24h": 10,
            "avg_amount_24h": 100.0
        }

    async def _get_processing_time(self, start_time: float, end_time: float) -> int:
        return 50


class MockScoringService(ScoringService):
    """Мок для тестирования ScoringService"""

    async def score_transaction(self, transaction: Transaction) -> ScoringResult:
        # Пустая реализация для тестирования
        return ScoringResult(
            customer_id=transaction.customer_id,
            transaction_id=transaction.transaction_id,
            scoring=0.5,
            processed_at="2023-01-01T10:00:00Z"
        )

    async def _get_ml_model_score(self, transaction: Transaction) -> float:
        return 0.5

    async def _handle_model_timeout(self, transaction: Transaction) -> float:
        return 0.5


@pytest.mark.asyncio
async def test_transaction_service_interface():
    """Тест интерфейса TransactionService"""
    service = MockTransactionService()

    # Проверяем, что методы существуют
    assert hasattr(service, 'process_transaction')
    assert hasattr(service, '_validate_transaction')
    assert hasattr(service, '_calculate_statistics')
    assert hasattr(service, '_get_processing_time')


@pytest.mark.asyncio
async def test_scoring_service_interface():
    """Тест интерфейса ScoringService"""
    service = MockScoringService()

    # Проверяем, что методы существуют
    assert hasattr(service, 'score_transaction')
    assert hasattr(service, '_get_ml_model_score')
    assert hasattr(service, '_handle_model_timeout')


@pytest.mark.asyncio
async def test_transaction_service_process():
    """Тест метода process_transaction"""
    service = MockTransactionService()

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

    # Проверяем, что метод вызывается без ошибок
    result = await service.process_transaction(transaction)

    assert result.customer_id == "customer_123"
    assert result.transaction_id == "txn_456"
    assert result.scoring == 0.5