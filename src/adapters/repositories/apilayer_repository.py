import requests
from pydantic import BaseModel

from src.commons.config import settings


class ApiLayerResponseError(Exception):
    pass


class ApiLayerQuoted(BaseModel):
    code: str
    price: float


class ApiLayerRepository:
    def __init__(self, url: str):
        self.api_url = url
        self.headers = {"apikey": settings.APILAYER_APIKEY}

    def latest(self, base: str, symbols: list[str]) -> list[ApiLayerQuoted]:
        params = {"base": base, "symbols": ",".join(symbols)}
        response = requests.request(
            "GET", f"{self.api_url}/latest", headers=self.headers, params=params
        )
        if not response.ok or not response.json()["success"]:
            raise ApiLayerResponseError(response.text)

        result = response.json()

        return [
            ApiLayerQuoted(code=code, price=price)
            for code, price in result["rates"].items()
        ]
