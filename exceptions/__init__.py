"""
Пользовательские исключения
"""

class AntifraudException(Exception):
    """Базовое исключение для антифрод сервиса"""
    pass

class TransactionProcessingError(AntifraudException):
    """Ошибка обработки транзакции"""
    pass

class ModelTimeoutError(AntifraudException):
    """Ошибка таймаута модели"""
    pass

class CacheError(AntifraudException):
    """Ошибка кэширования"""
    pass