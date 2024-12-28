import os
from typing import Union

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, FSInputFile, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaPhoto,
                           KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from django.conf import settings

from filters.chat_types import ChatTypeFilter
from keybords.inline import MenuCallBack, get_user_cart, get_user_main_btns
from keybords.reply import get_back_button
from queries.banner_queries import get_banner
from queries.cart_queries import clear_cart
from queries.order_queries import add_order, get_user_orders
from states.order_state import OrderState
from utils.utils import format_phone_number

order_router = Router()
order_router.message.filter(ChatTypeFilter(["private"]))


@order_router.callback_query(MenuCallBack.filter(F.menu_name == "order"))
async def start_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Please enter your name:")
    await state.set_state(OrderState.name)
    await callback.answer()


@order_router.message(OrderState.name, F.text)
async def process_name(message: types.Message, state: FSMContext):
    if len(message.text) < 2 or len(message.text) > 50:
        await message.answer(
            "Name must be between 2 and 50 characters. Please enter your name again:"
        )
        return
    await state.update_data(name=message.text)
    await message.answer(
        "Please enter your phone number:", reply_markup=get_back_button()
    )
    await state.set_state(OrderState.phone)


@order_router.message(OrderState.phone, F.text)
async def process_phone(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Back":
        await message.answer(
            "Please enter your name again:", reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(OrderState.name)
        return

    formatted_phone = format_phone_number(message.text)
    if not formatted_phone:
        await message.answer(
            "Invalid phone number. Please enter a valid phone number (10-15 digits):"
        )
        return

    await state.update_data(phone=formatted_phone)
    await message.answer(
        "Phone number accepted. Please enter your address:",
        reply_markup=get_back_button(),
    )
    await state.set_state(OrderState.address)


@order_router.message(OrderState.address, F.text)
async def process_address(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Back":
        await message.answer(
            "Please enter your phone number again:", reply_markup=get_back_button()
        )
        await state.set_state(OrderState.phone)
        return

    if len(message.text) < 5 or len(message.text) > 100:
        await message.answer(
            "Address must be between 5 and 100 characters. Please enter your address again:"
        )
        return

    await state.update_data(address=message.text)
    user_data = await state.get_data()

    confirmation_message = (
        f"Please confirm your order details:\n\n"
        f"Name: {user_data['name']}\n"
        f"Phone: {user_data['phone']}\n"
        f"Address: {user_data['address']}\n\n"
        "Is everything correct?"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Confirm ✅", callback_data="confirm_order"),
                InlineKeyboardButton(text="Cancel ❌", callback_data="cancel_order"),
            ]
        ]
    )

    await message.answer(confirmation_message, reply_markup=keyboard)
    await state.set_state(OrderState.confirm)


@order_router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await callback.answer("This order has already been processed!", show_alert=True)
        return

    try:
        user_data = await state.get_data()

        await add_order(
            user_id=callback.from_user.id,
            name=user_data.get("name", ""),
            phone=user_data.get("phone", ""),
            address=user_data.get("address", ""),
            status="pending",
        )

        await clear_cart(user_id=callback.from_user.id)

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            "Your order has been confirmed! ✅",
            reply_markup=get_user_main_btns(level=1),
        )

        await state.clear()
        await callback.answer("Order successfully created!", show_alert=True)

    except Exception as e:
        print(f"Error creating order: {e}")
        await callback.answer(
            "Error creating order. Please try again.", show_alert=True
        )


@order_router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await callback.answer("This order has already been processed!", show_alert=True)
        return

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    await callback.message.answer(
        "Order canceled ❌", reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()


@order_router.callback_query(F.data.startswith("edit_"))
async def handle_edit(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[1]
    if field == "name":
        await callback.message.answer(
            "Please enter your name again:", reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(OrderState.name)
    elif field == "phone":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="⬅️ Back")],
            ],
            resize_keyboard=True,
        )
        await callback.message.answer(
            "Please enter your phone number again:", reply_markup=keyboard
        )
        await state.set_state(OrderState.phone)
    elif field == "address":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="⬅️ Back")],
            ],
            resize_keyboard=True,
        )
        await callback.message.answer(
            "Please enter your address again:", reply_markup=keyboard
        )
        await state.set_state(OrderState.address)

    await callback.answer()


@order_router.message(Command("orders"))
@order_router.callback_query(MenuCallBack.filter(F.menu_name == "orders"))
async def process_orders_command(update: Union[CallbackQuery, Message]):
    try:
        if isinstance(update, CallbackQuery):
            user_id = update.from_user.id
            target = update.message
            is_callback = True
        else:
            user_id = update.from_user.id
            target = update
            is_callback = False

        orders = await get_user_orders(user_id)

        banner = await get_banner("orders")
        if not banner:
            raise ValueError("Banner not found")

        if not banner.image:
            raise ValueError("Banner has no image")

        image_path = os.path.join(settings.MEDIA_ROOT, str(banner.image))
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Banner image not found: {image_path}")

        if not orders:
            media = InputMediaPhoto(
                media=FSInputFile(image_path),
                caption=f"<strong>{banner.description}</strong>",
                parse_mode="HTML"
            )

            kbds = get_user_cart(
                level=1,
                page=None,
                pagination_btns=None,
                product_id=None,
            )

            if is_callback:
                await target.edit_media(media=media, reply_markup=kbds)
                await update.answer()
            else:
                await target.answer_photo(
                    photo=FSInputFile(image_path),
                    caption=f"<strong>{banner.description}</strong>",
                    reply_markup=kbds,
                    parse_mode="HTML",
                )
        else:
            text = ""
            for order in orders:
                text += (
                    f"🔸 Заказ {order.id}\n"
                    f"👤 Имя: {order.name}\n"
                    f"📦 Статус: {order.status}\n"
                    f"📍 Адрес: {order.address}\n"
                    f"📱 Телефон: {order.phone}\n"
                    f"-------------------\n"
                )

            media = InputMediaPhoto(
                media=FSInputFile(image_path),
                caption=f"<strong>{banner.description}</strong>\n\n{text}",
                parse_mode="HTML"
            )

            if is_callback:
                await target.edit_media(
                    media=media,
                    reply_markup=get_user_main_btns(level=1)
                )
                await update.answer()
            else:
                await target.answer_photo(
                    photo=FSInputFile(image_path),
                    caption=f"<strong>{banner.description}</strong>\n\n{text}",
                    reply_markup=get_user_main_btns(level=1),
                    parse_mode="HTML",
                )

    except Exception as e:
        if is_callback:
            await update.answer(
                "Произошла ошибка при получении заказов",
                show_alert=True
            )
        else:
            await target.answer(
                "Произошла ошибка при получении заказов. "
            )
