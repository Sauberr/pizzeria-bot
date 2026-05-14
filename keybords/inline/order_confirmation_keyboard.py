import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner


def get_order_confirmation_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    user_agreement_url = os.getenv("USER_AGREEMENT")

    rows = [
        [
            InlineKeyboardButton(
                text=i18n.select_payment_btn(),
                callback_data="select_payment",
            ),
            InlineKeyboardButton(
                text=i18n.cancel_order_btn(),
                callback_data="cancel_order",
            ),
        ]
    ]

    if user_agreement_url:
        rows.append(
            [
                InlineKeyboardButton(
                    text=i18n.user_agreement_btn(),
                    url=user_agreement_url,
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=rows)