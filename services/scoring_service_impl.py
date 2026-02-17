"""
Реализация сервиса оценки транзакций с использованием ML модели
"""
import asyncio
import random
from datetime import datetime
from typing import Optional
from models.transaction import Transaction
from models.scoring import ScoringResult
from services.scoring_service import ScoringService
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ScoringServiceImpl(ScoringService):
    """Реализация сервиса оценки транзакций"""

    def __init__(self):
        self._model_timeout_ms = settings.ML_MODEL_TIMEOUT_MS
        self._default_score = settings.DEFAULT_SCORING_VALUE

    async def score_transaction(self, transaction: Transaction) -> ScoringResult:
        """
        Оценить транзакцию с помощью ML модели

        Args:
            transaction: Транзакция для оценки

        Returns:
            Результат оценки транзакции
        """
        logger.info(f"Начало оценки транзакции {transaction.transaction_id}")

        try:
            # Получаем оценку от ML модели
            score = await self._get_ml_model_score(transaction)

            # Определяем is_fraud на основе порога
            is_fraud = score > 0.7

            logger.info(
                f"Оценка транзакции {transaction.transaction_id} завершена. "
                f"Score: {score:.4f}, Is Fraud: {is_fraud}"
            )

            return ScoringResult(
                customer_id=transaction.customer_id,
                transaction_id=transaction.transaction_id,
                scoring=score,
                is_fraud=is_fraud,
                processed_at=datetime.utcnow().isoformat() + "Z"
            )

        except asyncio.TimeoutError:
            logger.warning(
                f"Таймаут при оценке транзакции {transaction.transaction_id}"
            )
            return await self._handle_model_timeout(transaction)
        except Exception as e:
            logger.error(
                f"Ошибка при оценке транзакции {transaction.transaction_id}: {str(e)}"
            )
            return await self._handle_model_timeout(transaction)

    async def _get_ml_model_score(self, transaction: Transaction) -> float:
        """
        Получить оценку от ML модели

        В реальной системе здесь будет вызов ML модели.
        Для демонстрации используется симуляция с элементом случайности.

        Args:
            transaction: Транзакция для оценки

        Returns:
            Оценка от 0 до 1
        """
        # Симуляция асинхронного вызова ML модели
        # В production здесь будет HTTP/gRPC вызов к ML сервису
        await asyncio.sleep(0.01)  # 10ms симуляция

        # Базовый scoring на основе характеристик транзакции
        base_score = 0.3  # Базовый риск

        # Учитываем сумму транзакции (высокие суммы - выше риск)
        if transaction.amount > 1000:
            base_score += 0.2
        elif transaction.amount > 500:
            base_score += 0.1

        # Учитываем тип транзакции
        if transaction.type in [78, 80, 85]:  # Высокий риск типов
            base_score += 0.15

        # Учитываем флаги риска, если они есть
        if transaction.is_velocity_alert:
            base_score += 0.2
        if transaction.is_location_alert:
            base_score += 0.15
        if transaction.is_device_alert:
            base_score += 0.1

        # Добавляем небольшую случайность для демонстрации
        random_factor = random.uniform(-0.05, 0.05)
        final_score = min(max(base_score + random_factor, 0.0), 1.0)

        return final_score

    async def _handle_model_timeout(self, transaction: Transaction) -> ScoringResult:
        """
        Обработка таймаута модели

        Args:
            transaction: Транзакция для оценки

        Returns:
            Результат оценки по умолчанию
        """
        logger.warning(
            f"Используется значение по умолчанию для транзакции "
            f"{transaction.transaction_id} из-за таймаута модели"
        )
        
        return ScoringResult(
            customer_id=transaction.customer_id,
            transaction_id=transaction.transaction_id,
            scoring=self._default_score,
            is_fraud=False,
            processed_at=datetime.utcnow().isoformat() + "Z"
        )
