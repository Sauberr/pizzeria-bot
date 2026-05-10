from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from fluentogram import TranslatorRunner


def get_reply_back_button(i18n: TranslatorRunner):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=i18n.back_button())]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
