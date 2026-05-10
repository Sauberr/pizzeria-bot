from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from callbacks.callbacks import PromoCallBack


def get_promo_list_keyboard(promos, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for promo in promos:
        active_icon = "✅" if promo.is_active else "❌"
        builder.row(
            InlineKeyboardButton(
                text=f"✏️ {promo.code}",
                callback_data=PromoCallBack(action="edit", promo_id=promo.id).pack(),
            ),
            InlineKeyboardButton(
                text="🗑️",
                callback_data=PromoCallBack(action="delete", promo_id=promo.id).pack(),
            ),
            InlineKeyboardButton(
                text=active_icon,
                callback_data=PromoCallBack(action="toggle", promo_id=promo.id).pack(),
            ),
        )

    builder.row(
        InlineKeyboardButton(
            text=i18n.admin_promo_add_btn(),
            callback_data=PromoCallBack(action="add").pack(),
        )
    )

    return builder.as_markup()