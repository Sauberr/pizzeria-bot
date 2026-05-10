from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from app import CHANNEL_LINK


def get_subscription_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.subscribe_to_channel_button(), url=CHANNEL_LINK)],
            [InlineKeyboardButton(text=i18n.check_subscription_button(), callback_data="check_subscription")],
        ]
    )