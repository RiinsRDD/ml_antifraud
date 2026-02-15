"""
Сервис оценки транзакций с использованием ML модели
"""
from abc import ABC, abstractmethod
from typing import Optional
from models.transaction import Transaction
from models.scoring import ScoringResult

class ScoringService(ABC):
    """Абстрактный базовый класс сервиса оценки"""

    @abstractmethod
    async def score_transaction(self, transaction: Transaction) -> ScoringResult:
        """
        Оценить транзакцию с помощью ML модели

        Args:
            transaction: Транзакция для оценки

        Returns:
            Результат оценки транзакции

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def _get_ml_model_score(self, transaction: Transaction) -> float:
        """
        Получить оценку от ML модели

        Args:
            transaction: Транзакция для оценки

        Returns:
            Оценка от 0 до 1

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def _handle_model_timeout(self, transaction: Transaction) -> float:
        """
        Обработка таймаута модели

        Args:
            transaction: Транзакция для оценки

        Returns:
            Оценка по умолчанию

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...