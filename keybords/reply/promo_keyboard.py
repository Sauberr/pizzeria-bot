from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from fluentogram import TranslatorRunner


def get_promo_keyboard(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=i18n.promo_skip_button())],
            [KeyboardButton(text=i18n.back_button())],
        ],
        resize_keyboard=True,
    )