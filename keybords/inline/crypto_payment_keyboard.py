from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner



def get_crypto_payment_keyboard(crypto: str, bot_invoice_url: str, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.pay_with_crypto_btn(crypto=crypto),
                    url=bot_invoice_url,
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.cancel_order_btn(),
                    callback_data="cancel_order"
                )
            ],
        ]
    )