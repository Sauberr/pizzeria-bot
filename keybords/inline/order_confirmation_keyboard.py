import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner


def get_order_confirmation_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.select_payment_btn(),
                    callback_data="select_payment"
                ),
                InlineKeyboardButton(
                    text=i18n.cancel_order_btn(),
                    callback_data="cancel_order"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=i18n.user_agreement_btn(),
                    url=os.getenv("USER_AGREEMENT")
                )
            ],
        ]
    )