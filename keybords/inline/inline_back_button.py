from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from callbacks.callbacks import MenuCallBack


def get_inline_back_button(i18n: TranslatorRunner):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.back_button(),
                    callback_data=MenuCallBack(menu_name="main", level=1 - 1).pack(),
                )
            ]
        ]
    )