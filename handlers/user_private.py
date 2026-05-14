import asyncio
import logging
from typing import Union

from aiogram import Bot, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from filters.chat_types import ChatTypeFilter
from handlers.captcha import CaptchaManager
from handlers.menu_processing import get_menu_content
from callbacks.callbacks import MenuCallBack
from queries.banner_queries import get_banner
from queries.cart_queries import add_to_cart

logger = logging.getLogger(__name__)

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(
    Command(commands=["menu", "cart", "about", "payment", "shipping"])
)
@user_private_router.callback_query(MenuCallBack.filter())
async def process_menu_command(
    update: Union[CallbackQuery, Message],
    state: FSMContext,
    i18n: TranslatorRunner,
    user_language: str,
) -> None:
    try:
        user_id = update.from_user.id

        if not await CaptchaManager.has_passed_recently(user_id):
            target_message = (
                update.message if isinstance(update, CallbackQuery) else update
            )
            if isinstance(update, CallbackQuery):
                await update.answer(i18n.complete_captcha_first(), show_alert=True)
            await CaptchaManager.send_new_captcha(target_message, user_id, state, i18n)
            return

        if isinstance(update, CallbackQuery):
            if "add_to_cart" in update.data:
                callback_data = MenuCallBack.unpack(update.data)
                cart_item = await add_to_cart(
                    user_id=user_id, product_id=callback_data.product_id
                )
                await update.answer(
                    i18n.product_added_to_cart()
                    if cart_item
                    else i18n.error_adding_to_cart()
                )
                return

        if isinstance(update, CallbackQuery):
            callback_data = MenuCallBack.unpack(update.data)
            menu_name, level, category, page, product_id = (
                callback_data.menu_name,
                callback_data.level,
                callback_data.category,
                callback_data.page,
                callback_data.product_id,
            )
            target = update.message
            is_callback = True
        else:
            menu_name = update.text[1:]
            level, category, page, product_id = 0, None, 1, None
            target = update
            is_callback = False

        content, keyboard = await get_menu_content(
            level=level,
            menu_name=menu_name,
            i18n=i18n,
            user_language=user_language,
            category=category,
            page=page,
            product_id=product_id,
            user_id=user_id,
        )

        banner = await get_banner(menu_name) if level == 0 else None
        if banner and isinstance(content, types.InputMediaPhoto):
            content.caption = banner.description

        if is_callback:
            try:
                if isinstance(content, types.InputMediaPhoto):
                    await target.edit_media(media=content, reply_markup=keyboard)
                else:
                    await target.edit_text(
                        text=content, reply_markup=keyboard, parse_mode="HTML"
                    )
            except TelegramBadRequest:
                logger.warning("Failed to edit message, sending as new message instead.")
            finally:
                await update.answer()
        else:
            if isinstance(content, types.InputMediaPhoto):
                await target.answer_photo(
                    photo=content.media,
                    caption=content.caption,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
            else:
                await target.answer(
                    text=content, reply_markup=keyboard, parse_mode="HTML"
                )

    except Exception:
        if isinstance(update, CallbackQuery):
            await update.answer(i18n.unrecognized_action(), show_alert=True)


@user_private_router.message(Command("clear"))
async def clear_private_user(
    message: types.Message, bot: Bot, i18n: TranslatorRunner
) -> None:
    try:
        if message.chat.type != "private":
            return

        command, *args = message.text.split()
        num_messages = int(args[0]) if args and args[0].isdigit() else 10

        deleted_count = 0
        for i in range(num_messages):
            try:
                message_id = message.message_id - i
                await bot.delete_message(message.chat.id, message_id)
                deleted_count += 1
            except TelegramBadRequest:
                continue

        if deleted_count > 0:
            notification = await message.answer(
                i18n.messages_deleted(count=deleted_count)
            )
            await asyncio.sleep(3)
            try:
                await notification.delete()
            except TelegramBadRequest:
                pass

    except ValueError:
        await message.answer(i18n.invalid_clear_format())
