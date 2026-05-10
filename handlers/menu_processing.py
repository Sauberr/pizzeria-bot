import os
from typing import Any

from aiogram.types import FSInputFile, InputMediaPhoto
from django.conf import settings
from fluentogram import TranslatorRunner
from parler.utils.context import switch_language

from keybords.inline.user_cart import get_user_cart
from keybords.inline.user_catalog_btns import get_user_catalog_btns
from keybords.inline.user_main_btns import get_user_main_btns
from keybords.inline.products_btns import get_products_btns
from queries.cart_queries import (add_to_cart, delete_from_cart,
                                  get_user_carts, reduce_product_in_cart)
from queries.category_queries import get_categories
from queries.products_queries import get_products
from utils.get_banner_image import get_banner_image
from utils.paginator import Paginator
from utils.currency import  convert_currency, format_price


async def main_menu(level: int, menu_name: str, i18n: TranslatorRunner, user_language: str) -> tuple:
    image = await get_banner_image(menu_name, i18n)
    kbds = get_user_main_btns(level=level, i18n=i18n)
    return image, kbds


async def catalog(level: int, menu_name: str, i18n: Any, user_language: str) -> tuple:
    image = await get_banner_image(menu_name, i18n)
    categories = await get_categories()

    kbds = get_user_catalog_btns(
        level=level,
        categories=categories,
        i18n=i18n,
        user_language=user_language,
    )
    return image, kbds


async def pages(paginator: Paginator, i18n: TranslatorRunner) -> dict:
    btns = dict()
    if paginator.has_previous():
        btns[i18n.prev_button()] = "previous"

    if paginator.has_next():
        btns[i18n.next_button()] = "next"

    return btns


async def products(
    level: int, category: int, page: int, i18n: TranslatorRunner, user_language: str
) -> tuple:
    products = await get_products(category_id=category)

    paginator = Paginator(products, page)
    page_items = paginator.get_page()
    if not page_items:
        raise ValueError(i18n.product_no_image())
    product = page_items[0]
    with switch_language(product, user_language):
        converted_price, current_symbol = await convert_currency(
            product.price, user_language
        )
        formatted_price = format_price(converted_price, current_symbol)
        if product.image and os.path.exists(product.image.path):
            image = InputMediaPhoto(
                media=FSInputFile(product.image.path),
                caption=i18n.product_details(
                    name=product.name,
                    description=product.description,
                    price=formatted_price,
                    current_page=paginator.page,
                    total_pages=paginator.pages,
                ),
            )
        else:
            raise ValueError(i18n.product_no_image())

    pagination_btns = await pages(paginator, i18n=i18n)

    kbds = get_products_btns(
        level=level,
        i18n=i18n,
        category=category,
        page=page,
        pagination_btns=pagination_btns,
        product_id=product.id,
        user_language=user_language,
    )

    return image, kbds


async def carts(
    level,
    menu_name,
    page,
    user_id,
    product_id,
    i18n: TranslatorRunner,
    user_language: str,
):
    if menu_name == "delete":
        await delete_from_cart(user_id, product_id)
        if page > 1:
            page -= 1
    elif menu_name == "decrement":
        is_cart = await reduce_product_in_cart(user_id, product_id)
        if page > 1 and not is_cart:
            page -= 1
    elif menu_name == "increment":
        await add_to_cart(user_id, product_id)

    carts = await get_user_carts(user_id)

    if not carts:
        image = await get_banner_image("cart", i18n)
        kbds = get_user_cart(
            level=level, i18n=i18n, page=None, pagination_btns=None, product_id=None
        )

    else:
        paginator = Paginator(carts, page=page)
        cart = paginator.get_page()[0]

        converted_product_price, currency_symbol = await convert_currency(
            cart.product.price, user_language
        )
        formatted_product_price = format_price(converted_product_price, currency_symbol)

        cart_price = cart.quantity * converted_product_price
        formatted_cart_price = format_price(cart_price, currency_symbol)

        total_usd = sum(float(c.product.price) * c.quantity for c in carts)
        total_price, _ = await convert_currency(total_usd, user_language)
        formatted_total_price = format_price(total_price, currency_symbol)

        if cart.product.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(cart.product.image))
            if os.path.exists(image_path):
                with switch_language(cart.product, user_language):
                    product_name = cart.product.name
                image = InputMediaPhoto(
                    media=FSInputFile(image_path),
                    caption=i18n.cart_item_details(
                        name=product_name,
                        price=formatted_product_price,
                        quantity=cart.quantity,
                        cart_price=formatted_cart_price,
                        current_page=paginator.page,
                        total_pages=paginator.pages,
                        total_price=formatted_total_price,
                    ),
                )
            else:
                raise FileNotFoundError(i18n.product_image_not_found(path=image_path))
        else:
            raise ValueError(i18n.product_no_image())

        pagination_btns = await pages(paginator, i18n=i18n)

        kbds = get_user_cart(
            level=level,
            i18n=i18n,
            page=page,
            pagination_btns=pagination_btns,
            product_id=cart.product.id,
        )

    return image, kbds


async def get_menu_content(
    level: int,
    menu_name: str,
    i18n,
    category: int | None = None,
    page: int | None = None,
    product_id: int | None = None,
    user_id: int | None = None,
    user_language: str = "en",
):
    if level == 0:
        return await main_menu(level, menu_name, i18n=i18n, user_language=user_language)
    elif level == 1:
        return await catalog(level, menu_name, i18n=i18n, user_language=user_language)
    elif level == 2:
        return await products(
            level, category, page, i18n=i18n, user_language=user_language
        )
    elif level == 3:
        return await carts(
            level,
            menu_name,
            page,
            user_id,
            product_id,
            i18n=i18n,
            user_language=user_language,
        )
