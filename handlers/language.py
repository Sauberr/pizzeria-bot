from aiogram import F, Router
from aiogram.types import CallbackQuery
from fluentogram import TranslatorHub, TranslatorRunner

from callbacks.callbacks import LanguageCallBack, MenuCallBack
from handlers.start_cmd import start_cmd
from keybords.inline.language_selection_keyboard import (
    get_language_selection_keyboard,
)
from queries.language_queries import set_user_language

language_router = Router()


@language_router.callback_query(MenuCallBack.filter(F.menu_name == "language"))
async def show_language_menu(callback: CallbackQuery, i18n: TranslatorRunner):
    await callback.message.edit_caption(
        text=i18n.select_language(), reply_markup=get_language_selection_keyboard(i18n)
    )


@language_router.callback_query(LanguageCallBack.filter())
async def change_language(
    callback: CallbackQuery,
    callback_data: LanguageCallBack,
    translator_hub: TranslatorHub,
):
    new_language = callback_data.language

    await set_user_language(callback.from_user.id, new_language)

    new_i18n = translator_hub.get_translator_by_locale(new_language)

    await callback.message.delete()
    await start_cmd(callback.message, new_i18n, new_language)
