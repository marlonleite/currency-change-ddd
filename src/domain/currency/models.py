from dataclasses import dataclass

from src.domain.model import IdentityModel


@dataclass
class Currency(IdentityModel):
    code: str

    def __hash__(self) -> int:
        return hash(self.id)

    @staticmethod
    def total_price(amount: float, price: float):
        return round(amount * price, 2)
