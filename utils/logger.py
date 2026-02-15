"""
Настройка логгирования
"""
import sys
from loguru import logger
from config.settings import settings

def setup_logger(name: str, level: str = None) -> logger:
    """
    Настройка логгера

    Args:
        name: Имя логгера
        level: Уровень логирования

    Returns:
        Настроенный логгер
    """
    # Удаляем стандартный handler
    logger.remove()

    # Добавляем новый handler с форматированием
    logger.add(
        sys.stdout,
        level=level or settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # Добавляем handler для файлов (если нужно)
    # logger.add(
    #     "logs/antifraud.log",
    #     rotation="500 MB",
    #     level="INFO",
    #     format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
    # )

    return logger