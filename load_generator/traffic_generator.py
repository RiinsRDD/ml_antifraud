"""
Генератор трафика для микросервиса антифрод оценки транзакций
Использует asyncio для асинхронной генерации нагрузки
"""
import asyncio
import random
import json
import time
from datetime import datetime, timedelta
import aiohttp
from typing import Dict, Any
from loguru import logger


class TrafficGenerator:
    """Класс для генерации трафика"""

    def __init__(self, base_url: str = "http://localhost:8000", max_transactions: int = 1000):
        """
        Инициализация генератора трафика

        Args:
            base_url: Базовый URL сервиса
            max_transactions: Максимальное количество транзакций в секунду
        """
        self.base_url = base_url
        self.max_transactions = max_transactions
        self.session = None
        self.running = False
        self.total_transactions = 0
        self.errors = 0

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def _generate_random_transaction(self) -> Dict[str, Any]:
        """
        Генерация случайной транзакции

        Returns:
            Словарь с данными транзакции
        """
        # Список возможных типов транзакций
        transaction_types = [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]

        # Список возможных валют
        currencies = ['USD', 'EUR', 'RUB', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF']

        # Список возможных каналов
        channels = ['online', 'mobile', 'pos', 'atm']

        # Список возможных локаций
        locations = ['US-NY', 'US-CA', 'US-TX', 'US-FL', 'US-WA', 'GB-LON', 'DE-BER', 'FR-PAR', 'JP-TOK', 'CN-BEI']

        # Генерация случайных данных
        transaction = {
            "customer_id": f"customer_{random.randint(1, 100000)}",
            "transaction_id": f"txn_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
            "amount": round(random.uniform(1.0, 10000.0), 2),
            "type": random.choice(transaction_types),
            "currency": random.choice(currencies),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "merchant_id": f"merchant_{random.randint(1, 10000)}",
            "card_bin": f"{random.randint(100000, 999999)}",
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "device_id": f"device_{random.randint(1, 1000000)}",
            "location": random.choice(locations),
            "channel": random.choice(channels),
            "merchant_risk_score": round(random.uniform(0.0, 1.0), 3),
            "card_risk_score": round(random.uniform(0.0, 1.0), 3),
            "customer_risk_score": round(random.uniform(0.0, 1.0), 3),
            "is_velocity_alert": random.choice([True, False]),
            "is_location_alert": random.choice([True, False]),
            "is_device_alert": random.choice([True, False]),
            "transaction_category": random.choice(['ecommerce', 'retail', 'atm', 'card', 'mobile', 'wire']),
            "is_high_value": random.choice([True, False])
        }

        return transaction

    async def send_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        """
        Отправка одной транзакции

        Args:
            transaction_data: Данные транзакции

        Returns:
            True если успешно, False в случае ошибки
        """
        try:
            url = f"{self.base_url}/api/v1/transactions"
            async with self.session.post(url, json=transaction_data, timeout=5) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.debug(f"Успешно обработана транзакция: {result['transaction_id']}")
                    return True
                else:
                    logger.error(f"Ошибка при отправке транзакции: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Исключение при отправке транзакции: {str(e)}")
            return False

    async def generate_traffic(self, duration_seconds: int = 60):
        """
        Генерация трафика в течение заданного времени

        Args:
            duration_seconds: Длительность генерации в секундах
        """
        logger.info(f"Запуск генератора трафика на {duration_seconds} секунд")

        start_time = time.time()
        self.running = True

        try:
            while self.running and (time.time() - start_time) < duration_seconds:
                # Рассчитываем количество транзакций в этом периоде
                transactions_per_second = min(self.max_transactions, 1000)

                # Генерируем транзакции
                tasks = []
                for _ in range(transactions_per_second):
                    transaction = self._generate_random_transaction()
                    task = self.send_transaction(transaction)
                    tasks.append(task)

                # Выполняем все запросы параллельно
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # Считаем ошибки и успешные запросы
                for result in results:
                    if isinstance(result, bool) and result:
                        self.total_transactions += 1
                    elif not isinstance(result, bool) or not result:
                        self.errors += 1

                # Вывод статистики каждые 10 секунд
                if int(time.time() - start_time) % 10 == 0:
                    logger.info(f"Статистика: {self.total_transactions} транзакций, {self.errors} ошибок")

                # Задержка для ограничения скорости (сохраняем нужное количество транзакций в секунду)
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            logger.info("Генерация трафика прервана пользователем")
        except Exception as e:
            logger.error(f"Ошибка в генерации трафика: {str(e)}")
        finally:
            self.running = False
            logger.info(f"Генерация трафика завершена. Всего: {self.total_transactions} транзакций, ошибок: {self.errors}")

    def stop(self):
        """Остановка генерации трафика"""
        self.running = False

    def get_stats(self) -> Dict[str, Any]:
        """
        Получение статистики генерации трафика

        Returns:
            Словарь со статистикой
        """
        return {
            "total_transactions": self.total_transactions,
            "errors": self.errors,
            "success_rate": self.total_transactions / (self.total_transactions + self.errors) if (self.total_transactions + self.errors) > 0 else 0
        }


async def main():
    """Основная функция для запуска генератора трафика"""
    async with TrafficGenerator(max_transactions=1000) as generator:
        await generator.generate_traffic(duration_seconds=60)


if __name__ == "__main__":
    asyncio.run(main())