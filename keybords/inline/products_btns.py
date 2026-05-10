from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from callbacks.callbacks import MenuCallBack


def get_products_btns(
    *,
    i18n: TranslatorRunner,
    level: int,
    category: int,
    page: int,
    user_language: str,
    pagination_btns: dict,
    product_id: int,
    sizes: tuple[int] = (2, 1),
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text=i18n.back_button(),
            callback_data=MenuCallBack(level=level - 1, menu_name="catalog").pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=i18n.cart_button(),
            callback_data=MenuCallBack(level=3, menu_name="cart").pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=i18n.buy_button(),
            callback_data=MenuCallBack(
                level=level, menu_name="add_to_cart", product_id=product_id
            ).pack(),
        )
    )

    keyboard.adjust(*sizes)

    row = []

    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        category=category,
                        page=page + 1,
                    ).pack(),
                )
            )

        elif menu_name == "previous":
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        category=category,
                        page=page - 1,
                    ).pack(),
                )
            )

    return keyboard.row(*row).as_markup()