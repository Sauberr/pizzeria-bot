from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluentogram import TranslatorRunner


def get_star_payment_keyboard(stars_amount: int, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.pay_with_stars_btn(stars_amount=stars_amount),
                    pay=True,
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.cancel_order_btn(), callback_data="cancel_order"
                )
            ],
        ]
    )
