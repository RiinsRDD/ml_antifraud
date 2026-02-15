"""
Репозиторий для работы с транзакциями в Redis
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from models.transaction import Transaction

class TransactionRepository(ABC):
    """Абстрактный базовый класс репозитория транзакций"""

    @abstractmethod
    async def add_transaction(self, transaction: Transaction) -> None:
        """
        Добавить транзакцию в кэш

        Args:
            transaction: Транзакция для добавления

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def get_transactions_by_customer(self, customer_id: str) -> List[Transaction]:
        """
        Получить все транзакции по customer_id

        Args:
            customer_id: ID клиента

        Returns:
            Список транзакций

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def get_statistics_by_customer(self, customer_id: str) -> Dict:
        """
        Получить статистику по customer_id

        Args:
            customer_id: ID клиента

        Returns:
            Словарь со статистикой

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def update_statistics(self, customer_id: str, stats: Dict) -> None:
        """
        Обновить статистику по customer_id

        Args:
            customer_id: ID клиента
            stats: Статистика для обновления

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def get_cached_transaction(self, customer_id: str) -> Optional[Transaction]:
        """
        Получить транзакцию по customer_id из кэша

        Args:
            customer_id: ID клиента

        Returns:
            Транзакция или None

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...

    @abstractmethod
    async def delete_expired_transactions(self) -> None:
        """
        Удалить истекшие транзакции из кэша

        Raises:
            NotImplementedError: Если метод не реализован
        """
        ...