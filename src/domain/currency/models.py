from dataclasses import dataclass

from src.domain.model import IdentityModel


@dataclass
class Currency(IdentityModel):
    code: str
    name: str
