from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner


def get_select_payment_keyboard(i18n: TranslatorRunner):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="TON 💎", callback_data="crypto_TON"),
                InlineKeyboardButton(text="BTC ₿", callback_data="crypto_BTC"),
            ],
            [
                InlineKeyboardButton(text="USDT 💵", callback_data="crypto_USDT"),
                InlineKeyboardButton(text="ETH ⟠", callback_data="crypto_ETH"),
            ],
            [
                InlineKeyboardButton(
                    text=i18n.star_payment_btn(), callback_data="star_payment"
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.back_button(), callback_data="cancel_order"
                )
            ],
        ]
    )
