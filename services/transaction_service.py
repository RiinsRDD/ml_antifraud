"""
Сервис обработки транзакций
"""
from abc import ABC, abstractmethod
from typing import Optional
from models.transaction import Transaction
from models.scoring import ScoringResult

class TransactionService(ABC):
    """Абстрактный базовый класс сервиса транзакций"""

    @abstractmethod
    async def process_transaction(self, transaction: Transaction) -> ScoringResult:
        """
        Обработать транзакцию и вернуть результат оценки

        Args:
            transaction: Входящая транзакция

        Returns:
            Результат оценки транзакции

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def _validate_transaction(self, transaction: Transaction) -> bool:
        """
        Валидация транзакции

        Args:
            transaction: Транзакция для валидации

        Returns:
            Результат валидации

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def _calculate_statistics(self, customer_id: str) -> dict:
        """
        Расчет статистики по клиенту

        Args:
            customer_id: ID клиента

        Returns:
            Словарь со статистикой

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def _get_processing_time(self, start_time: float, end_time: float) -> int:
        """
        Расчет времени обработки

        Args:
            start_time: Время начала
            end_time: Время окончания

        Returns:
            Время обработки в миллисекундах

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...