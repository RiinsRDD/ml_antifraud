"""
Redis реализация репозитория транзакций
"""
import json
from typing import List, Dict, Optional
import redis.asyncio as redis
from models.transaction import Transaction
from repositories.transaction_repository import TransactionRepository
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RedisTransactionRepository(TransactionRepository):
    """Реализация репозитория транзакций с использованием Redis"""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        db: int = None,
        password: str = None
    ):
        self._host = host or settings.REDIS_HOST
        self._port = port or settings.REDIS_PORT
        self._db = db or settings.REDIS_DB
        self._password = password or settings.REDIS_PASSWORD
        self._pool: Optional[redis.ConnectionPool] = None
        self._client: Optional[redis.Redis] = None

    async def _get_client(self) -> redis.Redis:
        """Получение или создание клиента Redis с пулом соединений"""
        if self._client is None:
            self._pool = redis.ConnectionPool(
                host=self._host,
                port=self._port,
                db=self._db,
                password=self._password,
                max_connections=50,
                decode_responses=True
            )
            self._client = redis.Redis(connection_pool=self._pool)
        return self._client

    def _transaction_key(self, customer_id: str) -> str:
        """Ключ для хранения транзакций клиента"""
        return f"transactions:{customer_id}"

    def _stats_key(self, customer_id: str) -> str:
        """Ключ для хранения статистики клиента"""
        return f"stats:{customer_id}"

    async def add_transaction(self, transaction: Transaction) -> None:
        """Добавить транзакцию в кэш"""
        client = await self._get_client()
        key = self._transaction_key(transaction.customer_id)
        
        transaction_dict = transaction.model_dump()
        transaction_json = json.dumps(transaction_dict)
        
        # Добавляем в список транзакций с TTL
        await client.rpush(key, transaction_json)
        await client.expire(key, settings.CACHE_TTL)
        
        logger.info(
            f"Транзакция {transaction.transaction_id} добавлена в кэш "
            f"для клиента {transaction.customer_id}"
        )

    async def get_transactions_by_customer(self, customer_id: str) -> List[Transaction]:
        """Получить все транзакции по customer_id"""
        client = await self._get_client()
        key = self._transaction_key(customer_id)
        
        transactions_json = await client.lrange(key, 0, -1)
        
        transactions = []
        for txn_json in transactions_json:
            txn_dict = json.loads(txn_json)
            transactions.append(Transaction(**txn_dict))
        
        logger.info(
            f"Получено {len(transactions)} транзакций для клиента {customer_id}"
        )
        return transactions

    async def get_statistics_by_customer(self, customer_id: str) -> Dict:
        """Получить статистику по customer_id"""
        client = await self._get_client()
        key = self._stats_key(customer_id)
        
        stats_json = await client.get(key)
        
        if stats_json:
            return json.loads(stats_json)
        
        # Возвращаем статистику по умолчанию
        return {
            "total_transactions": 0,
            "total_amount": 0.0,
            "avg_amount": 0.0,
            "transaction_count_by_type": {},
            "last_transaction_time": None
        }

    async def update_statistics(self, customer_id: str, stats: Dict) -> None:
        """Обновить статистику по customer_id"""
        client = await self._get_client()
        key = self._stats_key(customer_id)
        
        await client.set(
            key,
            json.dumps(stats),
            ex=settings.CACHE_TTL
        )
        
        logger.info(f"Статистика обновлена для клиента {customer_id}")

    async def get_cached_transaction(self, customer_id: str) -> Optional[Transaction]:
        """Получить последнюю транзакцию по customer_id из кэша"""
        client = await self._get_client()
        key = self._transaction_key(customer_id)
        
        last_txn_json = await client.lindex(key, -1)
        
        if last_txn_json:
            txn_dict = json.loads(last_txn_json)
            return Transaction(**txn_dict)
        
        return None

    async def delete_expired_transactions(self) -> None:
        """Удалить истекшие транзакции из кэша"""
        # Redis автоматически удаляет ключи по TTL
        # Этот метод можно использовать для ручной очистки при необходимости
        logger.info("Проверка истекших транзакций (автоматически управляется Redis TTL)")

    async def close(self) -> None:
        """Закрыть соединение с Redis"""
        if self._client:
            await self._client.aclose()
        if self._pool:
            await self._pool.disconnect()
        logger.info("Соединение с Redis закрыто")