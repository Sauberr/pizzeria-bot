from typing import Union

from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, Message, ReplyKeyboardRemove)
from django.utils import timezone
from fluentogram import TranslatorRunner
from phonenumbers import NumberParseException

from filters.chat_types import ChatTypeFilter
from handlers.captcha import CaptchaManager
from handlers.check_subscription import CheckSubscription
from keybords.inline.subscription_keyboard import get_subscription_keyboard
from handlers.start_cmd import start_cmd
from callbacks.callbacks import MenuCallBack
from keybords.inline.inline_back_button import get_inline_back_button
from keybords.reply.reply_back_button import get_reply_back_button
from queries.captcha_queries import get_captcha_status
from queries.order_queries import get_user_orders
from queries.user_queries import create_telegram_user, get_user
from states.registration_state import RegistrationStates
from utils.get_banner_image import get_banner_image
from utils.phone_formatting import format_phone_number


registration_router = Router()
registration_router.message.filter(ChatTypeFilter(["private"]))


@registration_router.message(CommandStart())
async def start_registration(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner, user_language: str = "en"
):
    user_id = message.from_user.id

    if not await CaptchaManager.has_passed_recently(user_id):
        await CaptchaManager.send_new_captcha(message, user_id, i18n)
        return

    user = await get_user(user_id)
    if user and user.phone_number:
        await start_cmd(message, i18n, user_language)
    else:
        await message.answer(i18n.first_name_request())
        await state.set_state(RegistrationStates.first_name)


@registration_router.message(StateFilter(RegistrationStates.first_name))
async def process_first_name(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
):
    if len(message.text) > 30:
        await message.answer(i18n.name_too_long())
        return

    await state.update_data(first_name=message.text)
    await state.set_state(RegistrationStates.phone)
    await message.answer(
        i18n.phone_request(),
        reply_markup=get_reply_back_button(i18n=i18n),
        parse_mode="HTML",
    )


@registration_router.message(StateFilter(RegistrationStates.phone))
async def process_phone(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner, user_language: str = "en"
):
    if message.text == i18n.back_button():
        await state.set_state(RegistrationStates.first_name)
        await message.answer(
            i18n.first_name_request(), reply_markup=ReplyKeyboardRemove()
        )
        return

    try:
        formatted_phone = format_phone_number(message.text)
        if not formatted_phone:
            await message.answer(i18n.invalid_phone_format())
            return

        user_data = await state.get_data()

        user_id = message.from_user.id
        user = await create_telegram_user(
            user_id=user_id,
            first_name=user_data["first_name"],
            phone_number=formatted_phone,
        )

        if not user:
            await message.answer(i18n.phone_already_registered())
            return

        await state.clear()

        await message.answer(
            i18n.registration_complete_with_data(
                name=user_data["first_name"], phone=formatted_phone
            )
        )

        if await CheckSubscription.check_member_subscription(user_id):
            await start_cmd(message, i18n, user_language)
        else:
            await message.answer(
                i18n.subscription_required(),
                reply_markup=get_subscription_keyboard(i18n),
            )

    except NumberParseException:
        await message.answer(i18n.invalid_phone_format_intl())
    except ValueError:
        await message.answer(i18n.invalid_phone_retry())
    except Exception:
        await message.answer(i18n.registration_error())


@registration_router.message(Command("profile"))
@registration_router.callback_query(MenuCallBack.filter(F.menu_name == "profile"))
async def process_profile_command(
    update: Union[CallbackQuery, Message], i18n: TranslatorRunner, user_language: str
):
    try:
        user_id = update.from_user.id
        target = update.message if isinstance(update, CallbackQuery) else update
        user = await get_user(user_id)
        if not user:
            raise ValueError("User not found in database")

        orders = await get_user_orders(user_id)
        captcha_status = await get_captcha_status(user_id)

        is_passed = captcha_status and captcha_status.is_passed
        captcha_status_text = (
            i18n.captcha_passed() if is_passed else i18n.captcha_not_passed()
        )
        days_in_bot = (timezone.now() - user.created_at).days

        language_map = {"en": "🇬🇧", "ru": "🇷🇺"}
        user_language_flag = language_map.get(user.language, "🏳️")

        first_name = update.from_user.first_name or ""
        last_name = update.from_user.last_name or ""
        username = update.from_user.username or "N/A"

        profile_text = i18n.profile_text(
            user_id=str(user.id),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone=str(user.phone_number),
            captcha_status=captcha_status_text,
            language=user_language_flag,
            days_in_bot=days_in_bot,
            orders_count=len(orders),
            registration_date=user.created_at.strftime("%d.%m.%Y"),
        )

        media = await get_banner_image("profile", i18n)
        media.caption = profile_text

        if isinstance(update, CallbackQuery):
            keyboard = get_inline_back_button(i18n=i18n)
            await target.edit_media(media=media, reply_markup=keyboard)
            await update.answer()
        else:
            keyboard = get_reply_back_button(i18n=i18n)
            await target.answer_photo(
                photo=media.media, caption=media.caption, reply_markup=keyboard
            )

    except (ValueError, FileNotFoundError, AttributeError, OSError, TypeError) as e:
        error_message = str(e) or i18n.profile_load_error()

        if isinstance(update, CallbackQuery):
            await update.answer(error_message, show_alert=True)
        else:
            await update.answer(error_message)
