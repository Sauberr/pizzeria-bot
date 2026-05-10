from typing import Dict, List, Tuple
import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from callbacks.callbacks import LanguageCallBack, MenuCallBack


def get_language_selection_keyboard(i18n: TranslatorRunner):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇺🇸 English",
                    callback_data=LanguageCallBack(language="en").pack(),
                ),
                InlineKeyboardButton(
                    text="🇷🇺 Русский",
                    callback_data=LanguageCallBack(language="ru").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=i18n.back_button(),
                    callback_data=MenuCallBack(menu_name="main", level=0).pack(),
                )
            ],
        ]
    )