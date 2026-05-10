from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from app import CHANNEL_ID, bot
from handlers.menu_processing import get_menu_content
from keybords.inline.subscription_keyboard import get_subscription_keyboard

subscription_router = Router()


class CheckSubscription:
    @staticmethod
    async def check_member_subscription(user_id: int) -> bool:
        try:
            member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
            return member.status in ["creator", "administrator", "member"]
        except TelegramBadRequest:
            return False


@subscription_router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(
    callback: CallbackQuery, i18n: TranslatorRunner, user_language: str
):
    user_id = callback.from_user.id

    if await CheckSubscription.check_member_subscription(user_id):
        media, reply_markup = await get_menu_content(
            level=0, menu_name="main", i18n=i18n, user_language=user_language
        )
        await callback.message.answer_photo(
            media.media, caption=media.caption, reply_markup=reply_markup
        )
        await callback.message.delete()
        await callback.answer(i18n.subscription_successful())
    else:
        await callback.answer(i18n.subscription_required_callback())
