from src.commons.constants import Message
from src.commons.exceptions import AppException


class CurrencyError(AppException):
    @classmethod
    def message(cls, currency_id: int):
        return cls._message(currency_id=currency_id)

    @classmethod
    def create(cls, currency_id: int):
        return cls._create(currency_id=currency_id)


class CurrencyAlreadyExists(CurrencyError):
    public_message = Message.CURRENCY_ALREADY_EXISTS.value
    internal_message = "Currency already exists: currency_id={currency_id}"


class CurrencyNotFound(CurrencyError):
    public_message = Message.CURRENCY_NOT_FOUND.value
    internal_message = "Currency not found: currency_id={currency_id}"


class CurrencyConvertInconsistentError(AppException):
    public_message = Message.CURRENCY_CONVERT_INCONSISTENT_ERROR.value
    internal_message = "Currency not found: currency_code={currency_code}"

    @classmethod
    def message(cls, currency_code: str):
        return cls._message(currency_code=currency_code)

    @classmethod
    def create(cls, currency_code: str):
        return cls._create(currency_code=currency_code)
