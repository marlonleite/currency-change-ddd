from dataclasses import dataclass

from src.commons.abstracts.command import DomainCommand


@dataclass
class CreateCurrencyCommand(DomainCommand):
    code: str


@dataclass
class ConvertCurrencyCommand(DomainCommand):
    code: str
    amount: float
