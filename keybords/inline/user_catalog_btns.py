from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner
from parler.utils.context import switch_language

from callbacks.callbacks import MenuCallBack
from django_project.telegrambot.usersmanage.models import Category



def get_user_catalog_btns(
    *,
    i18n: TranslatorRunner,
    level: int,
    user_language: str,
    categories: list[Category],
    sizes: tuple[int] = (2,),
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text=i18n.back_button(),
            callback_data=MenuCallBack(level=level - 1, menu_name="main").pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=i18n.cart_button(),
            callback_data=MenuCallBack(level=3, menu_name="cart").pack(),
        )
    )
    for c in categories:
        with switch_language(c, user_language):
            keyboard.add(
                InlineKeyboardButton(
                    text=c.name,
                    callback_data=MenuCallBack(
                        level=level + 1, menu_name=c.name, category=c.id
                    ).pack(),
                )
            )

    return keyboard.adjust(*sizes).as_markup()