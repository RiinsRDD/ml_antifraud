"""
API маршруты для работы с транзакциями
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from models.transaction import Transaction
from models.scoring import ScoringResult
from services.transaction_service import TransactionService
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=ScoringResult, status_code=200)
async def process_transaction(
    transaction: Transaction,
    transaction_service: TransactionService = Depends()
):
    """
    Обработать транзакцию и вернуть оценку риска

    Args:
        transaction: Входящая транзакция
        transaction_service: Сервис обработки транзакций

    Returns:
        Результат оценки транзакции

    Raises:
        HTTPException: Если произошла ошибка обработки
    """
    logger.info(f"Получена транзакция: {transaction.transaction_id} от клиента: {transaction.customer_id}")

    try:
        # Обработка транзакции
        result = await transaction_service.process_transaction(transaction)
        logger.info(f"Оценка транзакции {transaction.transaction_id} завершена. Результат: {result.scoring}")
        return result
    except Exception as e:
        logger.error(f"Ошибка обработки транзакции {transaction.transaction_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка обработки транзакции: {str(e)}")