import logging
import os
import textwrap
from datetime import datetime

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, ReplyKeyboardRemove
from django.utils import timezone
from fluentogram import TranslatorRunner

from asgiref.sync import sync_to_async
from parler.utils.context import switch_language

from app import bot
from callbacks.callbacks import PromoCallBack
from django_project.telegrambot.usersmanage.models import TelegramUser
from filters.chat_types import ChatTypeFilter, IsAdmin
from filters.translated_text import TranslatedText
from keybords.inline.callback_btns import get_callback_btns
from keybords.inline.promo_management_keyboard import get_promo_list_keyboard
from keybords.reply.admin_keyboard import get_admin_keyboard
from queries.banner_queries import change_banner_image, get_info_pages
from queries.category_queries import get_categories
from queries.order_queries import total_orders
from queries.products_queries import (add_product, delete_product, get_product,
                                      get_products, total_products,
                                      total_products_by_category,
                                      update_product)
from queries.promo_queries import (create_promo_code, delete_promo_code_by_id,
                                   get_all_promo_codes, get_promo_by_id,
                                   toggle_promo_active, update_promo_code)
from queries.user_queries import total_users
from states.banner_state import AddBanner
from states.newsletter import Newsletter
from states.product_state import AddProduct
from states.promo_state import AddPromoCode
from utils.download_photo import download_telegram_photo

logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message, i18n: TranslatorRunner) -> None:
    admin_kb = get_admin_keyboard(i18n)
    await message.answer(i18n.admin_kb_placeholder(), reply_markup=admin_kb)


@admin_router.message(TranslatedText("admin_assortment"))
async def assortment_text(message: types.Message, i18n: TranslatorRunner):
    categories = await get_categories()
    btns = {category.name: f"category_{category.id}" for category in categories}
    await message.answer(
        i18n.admin_choose_category(), reply_markup=get_callback_btns(btns=btns)
    )


@admin_router.message(TranslatedText("admin_statistics"))
async def show_statistics(message: types.Message, i18n: TranslatorRunner):
    users = await total_users()
    orders = await total_orders()
    products = await total_products()
    category_stats = await total_products_by_category()

    category_stats_lines = [
        f"{category}: {count}" for category, count in category_stats.items()
    ]
    category_stats_text = textwrap.indent("\n".join(category_stats_lines), "        ")

    await message.answer(
        i18n.admin_statistics_text(
            users=users,
            orders=orders,
            products=products,
            category_stats_text=category_stats_text,
        )
    )


@admin_router.callback_query(F.data.startswith("category_"))
async def starring_at_product(callback: types.CallbackQuery, i18n: TranslatorRunner):
    try:
        category_id = callback.data.split("_")[-1]
        products = await get_products(int(category_id))

        for product in products:
            try:
                with switch_language(product, "en"):
                    caption = i18n.admin_product_card(
                        name=product.name,
                        description=product.description,
                        price=round(product.price, 2),
                    )
                reply_markup = get_callback_btns(
                    btns={
                        i18n.admin_delete_btn(): f"delete_{product.id}",
                        i18n.admin_edit_btn(): f"edit_{product.id}",
                    },
                    sizes=(2,),
                )
                if product.image and hasattr(product.image, "path"):
                    image_path = product.image.path
                    if os.path.exists(image_path):
                        photo = FSInputFile(image_path)
                        await callback.message.answer_photo(
                            photo=photo,
                            caption=caption,
                            reply_markup=reply_markup,
                        )
                else:
                    await callback.message.answer(
                        caption,
                        reply_markup=reply_markup,
                    )
            except (FileNotFoundError, AttributeError, OSError, TypeError):
                continue

        await callback.answer()
        await callback.message.answer(i18n.admin_products_list())

    except (FileNotFoundError, AttributeError, OSError, TypeError):
        await callback.message.answer(i18n.admin_products_error())
        await callback.answer()


@admin_router.callback_query(F.data.startswith("delete_"))
async def get_delete_product(callback: types.CallbackQuery, i18n: TranslatorRunner):
    product_id = callback.data.split("_")[-1]
    await delete_product(int(product_id))

    animation_url: str = os.getenv("DELETE_ANIMATION_URL")
    if animation_url:
        await callback.message.answer_animation(animation=animation_url)

    await callback.answer(i18n.admin_product_deleted())
    await callback.message.answer(i18n.admin_product_deleted())


@admin_router.message(StateFilter(None), TranslatedText("admin_add_banner"))
async def add_image_to_banner(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
) -> None:
    pages_names = [page.name for page in await get_info_pages()]
    await message.answer(i18n.admin_banner_instructions(pages=", ".join(pages_names)))
    await state.set_state(AddBanner.image)


@admin_router.message(AddBanner.image, F.photo)
async def add_banner(message: types.Message, state: FSMContext, i18n: TranslatorRunner) -> None:
    if not message.caption:
        await message.answer(i18n.admin_banner_wrong_page())
        return

    for_page = message.caption.strip()
    pages_names = [page.name for page in await get_info_pages()]
    if for_page not in pages_names:
        await message.answer(i18n.admin_banner_wrong_page())
        return

    try:
        save_path = await download_telegram_photo(message, "banners", for_page)

        await change_banner_image(for_page, save_path)

        await message.answer(i18n.admin_banner_success())

    except (FileNotFoundError, AttributeError, OSError, TypeError):
        await message.answer(i18n.admin_banner_error())
        return

    await state.clear()


@admin_router.message(AddBanner.image, or_f(F.photo, F.text == "."))
async def not_correct_add_banner(
    message: types.Message, i18n: TranslatorRunner
) -> None:
    await message.answer(i18n.admin_banner_wrong_data())


@admin_router.message(StateFilter("*"), Command("cancel"))
async def cancel_handler(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
) -> None:
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
    if AddPromoCode.promo_for_change:
        AddPromoCode.promo_for_change = None

    await state.clear()
    admin_kb = get_admin_keyboard(i18n)
    await message.answer(i18n.admin_canceled(), reply_markup=admin_kb)


@admin_router.message(StateFilter("*"), Command("back"))
async def back_step_handler(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
):
    current_state = await state.get_state()

    if current_state == AddProduct.en_name:
        await message.answer(i18n.admin_no_previous_step())
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            step_text = AddProduct.texts.get(previous.state, "")
            await message.answer(i18n.admin_previous_step(step_text=step_text))
            return
        previous = step


@admin_router.callback_query(StateFilter(None), F.data.startswith("edit_"))
async def edit_product_callback(
    callback: types.CallbackQuery, state: FSMContext, i18n: TranslatorRunner
):
    product_id = callback.data.split("_")[-1]
    product_for_change = await get_product(int(product_id))

    AddProduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        i18n.admin_product_edit_name(),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddProduct.en_name)


@admin_router.message(StateFilter(None), TranslatedText("admin_add_good"))
async def get_add_product(message: types.Message, state: FSMContext, i18n: TranslatorRunner):
    await message.answer(
        i18n.admin_product_add_en_name(),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddProduct.en_name)


@admin_router.message(AddProduct.en_name, or_f(F.text, F.text == "."))
async def add_en_name(message: types.Message, state: FSMContext, i18n: TranslatorRunner):
    if message.text == ".":
        await state.update_data(en_name=AddProduct.product_for_change.name_en if AddProduct.product_for_change else "")
    else:
        if not (4 <= len(message.text) <= 100):
            await message.answer(i18n.admin_product_name_error())
            return
        await state.update_data(en_name=message.text)

    await message.answer(i18n.admin_product_add_ru_name())
    await state.set_state(AddProduct.ru_name)


@admin_router.message(AddProduct.en_name)
async def not_correct_add_en_name(message: types.Message, i18n: TranslatorRunner):
    await message.answer(i18n.admin_product_name_wrong_data())


@admin_router.message(AddProduct.ru_name, or_f(F.text, F.text == "."))
async def add_ru_name(message: types.Message, state: FSMContext, i18n: TranslatorRunner):
    if message.text == ".":
        await state.update_data(ru_name=AddProduct.product_for_change.name_ru if AddProduct.product_for_change else "")
    else:
        if not (4 <= len(message.text) <= 100):
            await message.answer(i18n.admin_product_name_error())
            return
        await state.update_data(ru_name=message.text)

    await message.answer(i18n.admin_product_add_en_description())
    await state.set_state(AddProduct.en_description)


@admin_router.message(AddProduct.ru_name)
async def not_correct_add_ru_name(message: types.Message, i18n: TranslatorRunner):
    await message.answer(i18n.admin_product_name_wrong_data())


@admin_router.message(AddProduct.en_description, F.text)
async def add_en_description(message: types.Message, state: FSMContext, i18n: TranslatorRunner):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(en_description=AddProduct.product_for_change.description_en)
    else:
        if not (4 <= len(message.text) <= 1000):
            await message.answer(i18n.admin_product_description_error())
            return
        await state.update_data(en_description=message.text)

    await message.answer(i18n.admin_product_add_ru_description())
    await state.set_state(AddProduct.ru_description)


@admin_router.message(AddProduct.en_description)
async def not_correct_add_en_description(message: types.Message, i18n: TranslatorRunner):
    await message.answer(i18n.admin_product_description_wrong_data())


@admin_router.message(AddProduct.ru_description, F.text)
async def add_ru_description(message: types.Message, state: FSMContext, i18n: TranslatorRunner):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(ru_description=AddProduct.product_for_change.description_ru)
    else:
        if not (4 <= len(message.text) <= 1000):
            await message.answer(i18n.admin_product_description_error())
            return
        await state.update_data(ru_description=message.text)

    categories = await get_categories()
    btns = {category.name: str(category.id) for category in categories}
    await message.answer(i18n.admin_choose_category(), reply_markup=get_callback_btns(btns=btns))
    await state.set_state(AddProduct.category)


@admin_router.message(AddProduct.ru_description)
async def not_correct_add_ru_description(message: types.Message, i18n: TranslatorRunner):
    await message.answer(i18n.admin_product_description_wrong_data())


@admin_router.callback_query(AddProduct.category)
async def category_choice(callback: types.CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    if int(callback.data) in [category.id for category in await get_categories()]:
        await callback.answer()
        await state.update_data(category=callback.data)
        await callback.message.answer(i18n.admin_product_price())
        await state.set_state(AddProduct.price)
    else:
        await callback.message.answer(i18n.admin_category_wrong_choice())
        await callback.answer()


@admin_router.message(AddProduct.category)
async def not_correct_category_choice(message: types.Message, i18n: TranslatorRunner):
    await message.answer(i18n.admin_category_wrong_data())


@admin_router.message(AddProduct.price)
async def add_price(message: types.Message, state: FSMContext, i18n: TranslatorRunner):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer(i18n.admin_price_error())
            return
        await state.update_data(price=message.text)

    await message.answer(i18n.admin_product_image())
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.price)
async def not_correct_add_price(message: types.Message, i18n: TranslatorRunner):
    await message.answer(i18n.admin_product_price_wrong_data())


@admin_router.message(AddProduct.image, or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, i18n: TranslatorRunner) -> None:
    try:
        if message.text == "." and AddProduct.product_for_change:
            await state.update_data(
                image=(AddProduct.product_for_change.image.name if AddProduct.product_for_change.image else None)
            )
        elif message.photo:
            file_name = f"product_{int(datetime.now().timestamp())}"
            save_path = await download_telegram_photo(message, "products", file_name)
            await state.update_data(image=save_path)
        else:
            await message.answer(i18n.admin_image_keep_current())
            return

        data = await state.get_data()

        if AddProduct.product_for_change:
            if message.photo and AddProduct.product_for_change.image:
                old_image_path = AddProduct.product_for_change.image.path
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            await update_product(AddProduct.product_for_change.id, data)
        else:
            await add_product(data)

        admin_kb = get_admin_keyboard(i18n)
        await message.answer(i18n.admin_product_success(), reply_markup=admin_kb)
        await state.clear()
        AddProduct.product_for_change = None

    except (FileNotFoundError, AttributeError, OSError, TypeError):
        admin_kb = get_admin_keyboard(i18n)
        await message.answer(i18n.admin_product_error(), reply_markup=admin_kb)
        await state.clear()
        AddProduct.product_for_change = None


@admin_router.message(AddProduct.image)
async def not_correct_add_image(message: types.Message, i18n: TranslatorRunner):
    await message.answer(i18n.admin_product_image_wrong_data())


@admin_router.message(TranslatedText("admin_newsletter"))
async def newsletter(message: types.Message, state: FSMContext, i18n: TranslatorRunner):
    if message.from_user.id not in bot.my_admins_list:
        await message.answer(i18n.admin_no_access())
        return

    await state.set_state(Newsletter.waiting_for_content)
    await message.answer(i18n.admin_newsletter_content())


@admin_router.message(Newsletter.waiting_for_content)
async def process_newsletter(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
):
    users = await sync_to_async(list)(TelegramUser.objects.all())
    start_time = datetime.now()
    success_count = 0
    error_count = 0
    for user in users:
        try:
            await bot.send_message(
                user.user_id, message.text, parse_mode=message.parse_mode
            )
            success_count += 1
        except Exception:
            error_count += 1
            continue

    time_taken = (datetime.now() - start_time).total_seconds()
    await message.answer(
        i18n.admin_newsletter_success(
            success_count=success_count,
            error_count=error_count,
            time_taken=f"{time_taken:.2f}",
        ),
        parse_mode="HTML",
    )

    await state.clear()


# ═══════════════════════════════════════════════════════════════════════════════
# Promo Codes
# ═══════════════════════════════════════════════════════════════════════════════

def _format_promo_list(promos, i18n: TranslatorRunner) -> str:
    if not promos:
        return i18n.admin_promo_empty()

    now = timezone.now()
    lines = [i18n.admin_promo_list_header()]
    for promo in promos:
        if not promo.is_active:
            time_icon = "🔴"
        elif now < promo.valid_from:
            time_icon = "⏳"
        elif now > promo.valid_until:
            time_icon = "💀"
        else:
            time_icon = "🟢"

        max_uses_str = str(promo.max_uses) if promo.max_uses else "∞"
        lines.append(
            f"\n{time_icon} <b>{promo.code}</b> — {promo.discount_percent}%\n"
            f"   📅 {promo.valid_from.strftime('%d.%m.%Y')} – {promo.valid_until.strftime('%d.%m.%Y')}\n"
            f"   🔄 {promo.current_uses}/{max_uses_str}"
        )

    lines.append(i18n.admin_promo_legend())
    return "\n".join(lines)


async def _refresh_promo_list(callback: CallbackQuery, i18n: TranslatorRunner) -> None:
    promos = await get_all_promo_codes()
    text = _format_promo_list(promos, i18n)
    keyboard = get_promo_list_keyboard(promos, i18n)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")


@admin_router.message(StateFilter(None), TranslatedText("admin_promo_codes"))
async def show_promo_codes(message: types.Message, i18n: TranslatorRunner) -> None:
    promos = await get_all_promo_codes()
    text = _format_promo_list(promos, i18n)
    keyboard = get_promo_list_keyboard(promos, i18n)
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@admin_router.callback_query(PromoCallBack.filter(F.action == "list"))
async def refresh_promo_list(callback: CallbackQuery, i18n: TranslatorRunner) -> None:
    await _refresh_promo_list(callback, i18n)
    await callback.answer()


@admin_router.callback_query(PromoCallBack.filter(F.action == "toggle"))
async def toggle_promo(
    callback: CallbackQuery, callback_data: PromoCallBack, i18n: TranslatorRunner
) -> None:
    new_state = await toggle_promo_active(callback_data.promo_id)
    status_text = "✅" if new_state else "❌"
    await callback.answer(i18n.admin_promo_toggled(status=status_text))
    await _refresh_promo_list(callback, i18n)


@admin_router.callback_query(PromoCallBack.filter(F.action == "delete"))
async def delete_promo(
    callback: CallbackQuery, callback_data: PromoCallBack, i18n: TranslatorRunner
) -> None:
    await delete_promo_code_by_id(callback_data.promo_id)
    await callback.answer(i18n.admin_promo_deleted(), show_alert=True)
    await _refresh_promo_list(callback, i18n)


@admin_router.callback_query(StateFilter(None), PromoCallBack.filter(F.action == "add"))
async def start_add_promo(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner
) -> None:
    AddPromoCode.promo_for_change = None
    await callback.answer()
    await callback.message.answer(i18n.admin_promo_enter_code())
    await state.set_state(AddPromoCode.code)


@admin_router.callback_query(StateFilter(None), PromoCallBack.filter(F.action == "edit"))
async def start_edit_promo(
    callback: CallbackQuery,
    callback_data: PromoCallBack,
    state: FSMContext,
    i18n: TranslatorRunner,
) -> None:
    promo = await get_promo_by_id(callback_data.promo_id)
    if not promo:
        await callback.answer(i18n.admin_promo_not_found(), show_alert=True)
        return

    AddPromoCode.promo_for_change = promo
    await callback.answer()
    await callback.message.answer(i18n.admin_promo_edit_hint(current=promo.code))
    await state.set_state(AddPromoCode.code)


@admin_router.message(AddPromoCode.code, F.text)
async def promo_fsm_code(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
) -> None:
    if message.text == "." and AddPromoCode.promo_for_change:
        await state.update_data(code=AddPromoCode.promo_for_change.code)
    else:
        code = message.text.strip().upper()
        if not (2 <= len(code) <= 50):
            await message.answer(i18n.admin_promo_code_length_error())
            return
        await state.update_data(code=code)

    cur = AddPromoCode.promo_for_change
    hint = f" ({cur.discount_percent}%)" if cur else ""
    await message.answer(i18n.admin_promo_enter_discount(hint=hint))
    await state.set_state(AddPromoCode.discount_percent)


@admin_router.message(AddPromoCode.code)
async def promo_fsm_code_wrong(message: types.Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.admin_promo_enter_code())


@admin_router.message(AddPromoCode.discount_percent, F.text)
async def promo_fsm_discount(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
) -> None:
    if message.text == "." and AddPromoCode.promo_for_change:
        await state.update_data(
            discount_percent=float(AddPromoCode.promo_for_change.discount_percent)
        )
    else:
        try:
            val = float(message.text.replace(",", "."))
            if not (0 < val <= 100):
                raise ValueError
            await state.update_data(discount_percent=val)
        except ValueError:
            await message.answer(i18n.admin_promo_discount_error())
            return

    cur = AddPromoCode.promo_for_change
    hint = f" ({cur.valid_from.strftime('%d.%m.%Y')})" if cur else ""
    await message.answer(i18n.admin_promo_enter_valid_from(hint=hint))
    await state.set_state(AddPromoCode.valid_from)


@admin_router.message(AddPromoCode.discount_percent)
async def promo_fsm_discount_wrong(message: types.Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.admin_promo_discount_error())


@admin_router.message(AddPromoCode.valid_from, F.text)
async def promo_fsm_valid_from(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
) -> None:
    if message.text == "." and AddPromoCode.promo_for_change:
        await state.update_data(
            valid_from=AddPromoCode.promo_for_change.valid_from.isoformat()
        )
    else:
        try:
            dt = datetime.strptime(message.text.strip(), "%d.%m.%Y")
            aware_dt = timezone.make_aware(dt)
            await state.update_data(valid_from=aware_dt.isoformat())
        except ValueError:
            await message.answer(i18n.admin_promo_date_error())
            return

    cur = AddPromoCode.promo_for_change
    hint = f" ({cur.valid_until.strftime('%d.%m.%Y')})" if cur else ""
    await message.answer(i18n.admin_promo_enter_valid_until(hint=hint))
    await state.set_state(AddPromoCode.valid_until)


@admin_router.message(AddPromoCode.valid_from)
async def promo_fsm_valid_from_wrong(message: types.Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.admin_promo_date_error())


@admin_router.message(AddPromoCode.valid_until, F.text)
async def promo_fsm_valid_until(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
) -> None:
    if message.text == "." and AddPromoCode.promo_for_change:
        await state.update_data(
            valid_until=AddPromoCode.promo_for_change.valid_until.isoformat()
        )
    else:
        try:
            dt = datetime.strptime(message.text.strip(), "%d.%m.%Y")
            aware_dt = timezone.make_aware(dt)
            await state.update_data(valid_until=aware_dt.isoformat())
        except ValueError:
            await message.answer(i18n.admin_promo_date_error())
            return

    cur = AddPromoCode.promo_for_change
    hint = f" ({cur.max_uses or '∞'})" if cur else ""
    await message.answer(i18n.admin_promo_enter_max_uses(hint=hint))
    await state.set_state(AddPromoCode.max_uses)


@admin_router.message(AddPromoCode.valid_until)
async def promo_fsm_valid_until_wrong(message: types.Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.admin_promo_date_error())


@admin_router.message(AddPromoCode.max_uses, F.text)
async def promo_fsm_max_uses(
    message: types.Message, state: FSMContext, i18n: TranslatorRunner
) -> None:
    data = await state.get_data()

    if message.text == "." and AddPromoCode.promo_for_change:
        max_uses = AddPromoCode.promo_for_change.max_uses
    else:
        try:
            val = int(message.text.strip())
            if val < 0:
                raise ValueError
            max_uses = val if val > 0 else None
        except ValueError:
            await message.answer(i18n.admin_promo_max_uses_error())
            return

    valid_from = datetime.fromisoformat(data["valid_from"])
    valid_until = datetime.fromisoformat(data["valid_until"])

    if valid_until <= valid_from:
        await message.answer(i18n.admin_promo_date_range_error())
        await state.set_state(AddPromoCode.valid_from)
        return

    promo_data = {
        "code": data["code"],
        "discount_percent": data["discount_percent"],
        "valid_from": valid_from,
        "valid_until": valid_until,
        "max_uses": max_uses,
        "is_active": True,
    }

    try:
        if AddPromoCode.promo_for_change:
            await update_promo_code(AddPromoCode.promo_for_change.id, promo_data)
            result_text = i18n.admin_promo_updated()
        else:
            await create_promo_code(promo_data)
            result_text = i18n.admin_promo_created()
    except Exception:
        await message.answer(i18n.admin_promo_save_error())
        AddPromoCode.promo_for_change = None
        await state.clear()
        return

    AddPromoCode.promo_for_change = None
    await state.clear()
    await message.answer(result_text, reply_markup=get_admin_keyboard(i18n))


@admin_router.message(AddPromoCode.max_uses)
async def promo_fsm_max_uses_wrong(message: types.Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.admin_promo_max_uses_error())
