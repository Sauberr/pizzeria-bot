import asyncio

from aiogram import Bot, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from fluentogram import TranslatorRunner

from filters.chat_types import ChatTypeFilter
from utils.text_processing import clean_text, get_restricted_words

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))

restricted_words: set[str] = get_restricted_words()


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot) -> None:
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()


@user_group_router.message(Command("clear"))
async def clear_group(message: types.Message, bot: Bot, i18n: TranslatorRunner) -> None:
    if message.chat.type == "private":
        return
    try:
        chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status not in ["administrator", "creator"]:
            await message.answer(i18n.clear_admin_only())
            return

        bot_member = await bot.get_chat_member(message.chat.id, (await bot.me()).id)
        if not bot_member.can_delete_messages:
            await message.answer(i18n.bot_admin_required())
            return

        try:
            num_to_delete = (
                int(message.text.split()[1]) if len(message.text.split()) > 1 else 10
            )
        except (ValueError, IndexError):
            await message.answer(i18n.invalid_clear_format())
            return

        if num_to_delete < 1 or num_to_delete > 100:
            await message.answer(i18n.invalid_clear_format())
            return

        message_ids_to_delete = [
            message.message_id - i for i in range(num_to_delete + 1)
        ]

        await bot.delete_messages(
            chat_id=message.chat.id, message_ids=message_ids_to_delete
        )

        notification = await message.answer(i18n.messages_deleted(count=num_to_delete))
        await asyncio.sleep(3)
        await notification.delete()

    except TelegramBadRequest:
        await message.answer(i18n.clear_error())


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message, i18n: TranslatorRunner) -> None:
    if message.text and restricted_words.intersection(clean_text(message.text.lower()).split()):
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}"

        await message.answer(i18n.restricted_words_warning(user_name=full_name))

        await message.delete()
        await message.chat.ban(message.from_user.id)
