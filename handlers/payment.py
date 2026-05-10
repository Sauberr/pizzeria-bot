from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Union

import aiohttp

from app_config import env_config

_rate_cache: dict[str, tuple[float, datetime]] = {}
_CACHE_TTL = timedelta(minutes=5)


class CryptoApiManager:
    REQUEST_TIMEOUT: int = 10

    @classmethod
    async def _make_request(cls, url: str) -> Union[dict, None]:
        try:
            timeout = aiohttp.ClientTimeout(total=cls.REQUEST_TIMEOUT)
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == HTTPStatus.OK:
                        return await response.json()
                    return None
        except (ConnectionError, aiohttp.ClientError):
            return None

    @classmethod
    async def _get_cached_rate(cls, cache_key: str, url: str, response_key: str) -> Union[float, None]:
        cached = _rate_cache.get(cache_key)
        if cached and datetime.now() < cached[1]:
            return cached[0]
        data = await cls._make_request(url)
        if data and (rate := data.get(response_key)) is not None:
            rate = float(rate)
            _rate_cache[cache_key] = (rate, datetime.now() + _CACHE_TTL)
            return rate
        return None

    @classmethod
    async def get_crypto_rate(cls, crypto: str, fiat: str = "USD") -> Union[float, None]:
        url = f"{env_config.RATE_API_URL}?fsym={crypto}&tsyms={fiat}"
        return await cls._get_cached_rate(f"{crypto}_{fiat}", url, fiat)

    @classmethod
    async def convert_to_crypto(cls, amount: float, fiat: str, crypto: str) -> Union[float, None]:
        rate = await cls.get_crypto_rate(crypto, fiat)
        if rate is None:
            return None
        return amount / rate

    @classmethod
    async def get_usd_to_rub_rate(cls) -> Union[float, None]:
        url = f"{env_config.RATE_API_URL}?fsym=USD&tsyms=RUB"
        return await cls._get_cached_rate("USD_RUB", url, "RUB")