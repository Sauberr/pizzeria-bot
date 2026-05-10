from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram import TranslatorHub

from queries.language_queries import get_or_create_user_language


class I18nMiddleware(BaseMiddleware):
    def __init__(self, translator_hub: TranslatorHub):
        self.translator_hub = translator_hub

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = None
        if event.message:
            user = event.message.from_user
        elif event.edited_message:
            user = event.edited_message.from_user
        elif event.callback_query:
            user = event.callback_query.from_user
        elif event.inline_query:
            user = event.inline_query.from_user

        if user:
            data["user_language"] = await get_or_create_user_language(user.id)
            data["i18n"] = self.translator_hub.get_translator_by_locale(
                data["user_language"]
            )
            data["translator_hub"] = self.translator_hub
        else:
            data["user_language"] = self.translator_hub.root_locale
            data["i18n"] = self.translator_hub.get_translator_by_locale(
                data["user_language"]
            )
            data["translator_hub"] = self.translator_hub

        return await handler(event, data)
