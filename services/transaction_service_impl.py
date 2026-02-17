"""
Реализация сервиса обработки транзакций
"""
import time
from datetime import datetime
from typing import Dict
from models.transaction import Transaction
from models.scoring import ScoringResult
from repositories.transaction_repository import TransactionRepository
from services.transaction_service import TransactionService
from services.scoring_service import ScoringService
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TransactionServiceImpl(TransactionService):
    """Реализация сервиса обработки транзакций"""

    def __init__(
        self,
        repository: TransactionRepository,
        scoring_service: ScoringService
    ):
        self._repository = repository
        self._scoring_service = scoring_service

    async def process_transaction(self, transaction: Transaction) -> ScoringResult:
        """
        Обработать транзакцию и вернуть результат оценки

        Args:
            transaction: Входящая транзакция

        Returns:
            Результат оценки транзакции
        """
        start_time = time.time()
        
        logger.info(
            f"Начало обработки транзакции {transaction.transaction_id} "
            f"для клиента {transaction.customer_id}"
        )

        # Валидация транзакции
        is_valid = await self._validate_transaction(transaction)
        if not is_valid:
            logger.warning(f"Транзакция {transaction.transaction_id} не прошла валидацию")

        # Сохраняем транзакцию в кэш
        await self._repository.add_transaction(transaction)

        # Расчет статистики по клиенту
        customer_stats = await self._calculate_statistics(transaction.customer_id)

        # Вызов ML сервиса для оценки
        scoring_result = await self._scoring_service.score_transaction(transaction)

        # Расчет времени обработки
        end_time = time.time()
        processing_time_ms = await self._get_processing_time(start_time, end_time)

        # Формируем полный результат с статистикой
        result = ScoringResult(
            customer_id=transaction.customer_id,
            transaction_id=transaction.transaction_id,
            scoring=scoring_result.scoring,
            is_fraud=scoring_result.is_fraud,
            processing_time_ms=processing_time_ms,
            customer_transaction_count_24h=customer_stats.get("total_transactions", 0),
            customer_avg_amount_24h=customer_stats.get("avg_amount", 0.0),
            processed_at=datetime.utcnow().isoformat() + "Z"
        )

        logger.info(
            f"Обработка транзакции {transaction.transaction_id} завершена за "
            f"{processing_time_ms}ms. Результат: scoring={result.scoring:.4f}, "
            f"is_fraud={result.is_fraud}"
        )

        return result

    async def _validate_transaction(self, transaction: Transaction) -> bool:
        """
        Валидация транзакции

        Args:
            transaction: Транзакция для валидации

        Returns:
            Результат валидации
        """
        # Базовая валидация - все обязательные поля должны быть заполнены
        if not transaction.customer_id or not transaction.transaction_id:
            return False
        
        if transaction.amount <= 0:
            logger.warning(
                f"Некорректная сумма транзакции: {transaction.amount}"
            )
            return False

        if not transaction.currency or not transaction.merchant_id:
            return False

        return True

    async def _calculate_statistics(self, customer_id: str) -> Dict:
        """
        Расчет статистики по клиенту

        Args:
            customer_id: ID клиента

        Returns:
            Словарь со статистикой
        """
        # Получаем существующую статистику
        stats = await self._repository.get_statistics_by_customer(customer_id)

        # Получаем все транзакции клиента для пересчета
        transactions = await self._repository.get_transactions_by_customer(customer_id)

        if not transactions:
            return stats

        # Расчет статистики
        total_amount = sum(txn.amount for txn in transactions)
        total_count = len(transactions)
        avg_amount = total_amount / total_count if total_count > 0 else 0.0

        # Группировка по типам транзакций
        type_counts = {}
        for txn in transactions:
            type_counts[txn.type] = type_counts.get(txn.type, 0) + 1

        updated_stats = {
            "total_transactions": total_count,
            "total_amount": total_amount,
            "avg_amount": avg_amount,
            "transaction_count_by_type": type_counts,
            "last_transaction_time": transactions[-1].timestamp if transactions else None
        }

        # Сохраняем обновленную статистику
        await self._repository.update_statistics(customer_id, updated_stats)

        return updated_stats

    async def _get_processing_time(self, start_time: float, end_time: float) -> int:
        """
        Расчет времени обработки

        Args:
            start_time: Время начала
            end_time: Время окончания

        Returns:
            Время обработки в миллисекундах
        """
        return int((end_time - start_time) * 1000)