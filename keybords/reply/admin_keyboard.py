from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from fluentogram import TranslatorRunner


def get_admin_keyboard(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    button_keys = [
        "admin_add_good",
        "admin_assortment",
        "admin_add_banner",
        "admin_statistics",
        "admin_newsletter",
        "admin_promo_codes",
    ]

    for key in button_keys:
        builder.button(text=i18n.get(key))

    builder.adjust(2)

    return builder.as_markup(
        resize_keyboard=True, input_field_placeholder=i18n.admin_kb_placeholder()
    )
