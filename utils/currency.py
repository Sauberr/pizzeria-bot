from decimal import Decimal

from handlers.payment import CryptoApiManager


async def convert_currency(amount_usd, user_language: str) -> tuple[Decimal, str]:
    amount_usd = Decimal(str(amount_usd))
    if user_language == "ru":
        usd_to_rub = await CryptoApiManager.get_usd_to_rub_rate()
        if usd_to_rub is not None:
            return amount_usd * Decimal(str(usd_to_rub)), "₽"
    return amount_usd, "$"


def format_price(amount: Decimal, currency: str) -> str:
    if currency == "₽":
        return f"{amount:.0f} {currency}"
    else:
        return f"{amount:.2f} {currency}"
