from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

from utils.currency import convert_currency, format_price


def test_format_price_usd_two_decimals():
    assert format_price(Decimal("10.5"), "$") == "10.50 $"


def test_format_price_usd_rounds_correctly():
    assert format_price(Decimal("9.999"), "$") == "10.00 $"


def test_format_price_rub_no_decimals():
    assert format_price(Decimal("950"), "₽") == "950 ₽"


def test_format_price_rub_rounds_to_integer():
    assert format_price(Decimal("950.7"), "₽") == "951 ₽"


def test_format_price_zero_usd():
    assert format_price(Decimal("0"), "$") == "0.00 $"


def test_format_price_zero_rub():
    assert format_price(Decimal("0"), "₽") == "0 ₽"


@pytest.mark.asyncio
async def test_convert_currency_english_returns_usd():
    amount, symbol = await convert_currency(10, "en")
    assert symbol == "$"
    assert amount == Decimal("10")


@pytest.mark.asyncio
async def test_convert_currency_passes_decimal_correctly():
    amount, symbol = await convert_currency("25.50", "en")
    assert amount == Decimal("25.50")
    assert symbol == "$"


@pytest.mark.asyncio
async def test_convert_currency_russian_applies_rate():
    with patch(
        "utils.currency.CryptoApiManager.get_usd_to_rub_rate",
        new=AsyncMock(return_value=90.0),
    ):
        amount, symbol = await convert_currency(10, "ru")
    assert symbol == "₽"
    assert amount == Decimal("900.0")


@pytest.mark.asyncio
async def test_convert_currency_russian_fallback_to_usd_when_no_rate():
    with patch(
        "utils.currency.CryptoApiManager.get_usd_to_rub_rate",
        new=AsyncMock(return_value=None),
    ):
        amount, symbol = await convert_currency(10, "ru")
    assert symbol == "$"
    assert amount == Decimal("10")


@pytest.mark.asyncio
async def test_convert_currency_unknown_language_returns_usd():
    amount, symbol = await convert_currency(5, "de")
    assert symbol == "$"
