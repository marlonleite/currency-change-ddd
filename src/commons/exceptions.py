from typing import Any


class AppException(Exception):
    public_message: str
    internal_message: str = "Unset internal message: {provided}"

    @classmethod
    def _message(cls, **kwargs: Any):
        if cls.internal_message is None:
            provided = "| ".join(
                f"{str(key)}={str(value)}" for key, value in kwargs.items()
            )
            return cls.internal_message.format(provided=provided)
        return cls.internal_message.format(**kwargs)

    @classmethod
    def _create(cls, **kwargs: Any):
        if hasattr(cls, "message"):
            return cls(cls.message(**kwargs))  # type: ignore
        return cls(cls._message(**kwargs))
