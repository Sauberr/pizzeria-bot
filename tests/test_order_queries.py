import uuid
from decimal import Decimal

import pytest
from asgiref.sync import sync_to_async

from django_project.telegrambot.usersmanage.models import Cart, PromoCode
from queries.order_queries import (add_order_with_items, get_order_by_id,
                                   get_order_items, get_user_orders,
                                   total_orders)
from tests.conftest import make_category_async, make_promo_async, make_product_async, make_user_async


async def _create_cart_items(user, product, quantity=2):
    @sync_to_async
    def _create():
        return Cart.objects.create(user=user, product=product, quantity=quantity)

    cart = await _create()
    return [cart]


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_add_order_creates_order_and_items():
    user = await make_user_async(user_id=301001)
    product = await make_product_async(price="10.00")
    cart_items = await _create_cart_items(user, product, quantity=3)

    order = await add_order_with_items(
        user_id=user.user_id,
        name="John",
        phone="+380991234567",
        address="Kyiv, 1",
        status="pending",
        cart_items=cart_items,
    )

    assert order.pk is not None
    assert order.status == "pending"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_add_order_creates_correct_order_items():
    user = await make_user_async(user_id=301002, phone="+380991234568")
    product = await make_product_async(price="15.00")
    cart_items = await _create_cart_items(user, product, quantity=2)

    order = await add_order_with_items(
        user_id=user.user_id,
        name="Alice",
        phone="+380991234568",
        address="Lviv, 5",
        status="completed",
        cart_items=cart_items,
    )

    items = await get_order_items(order.id)
    assert len(items) == 1
    assert items[0].quantity == 2
    assert items[0].price == Decimal("15.00")


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_add_order_with_promo_saves_discount():
    user = await make_user_async(user_id=301003, phone="+380991234569")
    product = await make_product_async(price="20.00")
    cart_items = await _create_cart_items(user, product, quantity=1)
    promo = await make_promo_async(code="ORDTEST", discount=25)

    order = await add_order_with_items(
        user_id=user.user_id,
        name="Bob",
        phone="+380991234569",
        address="Odesa, 9",
        status="completed",
        cart_items=cart_items,
        promo_code_id=promo.id,
        discount_amount=5.0,
    )

    assert order.discount_amount == Decimal("5.0")
    assert order.promo_code_id == promo.id


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_add_order_with_promo_increments_uses():
    user = await make_user_async(user_id=301004, phone="+380991234570")
    product = await make_product_async(price="12.00")
    cart_items = await _create_cart_items(user, product)
    promo = await make_promo_async(code="INCR", discount=10, current_uses=3)

    await add_order_with_items(
        user_id=user.user_id,
        name="Eve",
        phone="+380991234570",
        address="Kharkiv, 2",
        status="completed",
        cart_items=cart_items,
        promo_code_id=promo.id,
        discount_amount=1.2,
    )

    @sync_to_async
    def _get():
        return PromoCode.objects.get(id=promo.id)

    updated_promo = await _get()
    assert updated_promo.current_uses == 4


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_add_order_without_promo_no_discount():
    user = await make_user_async(user_id=301005, phone="+380991234571")
    product = await make_product_async(price="8.00")
    cart_items = await _create_cart_items(user, product)

    order = await add_order_with_items(
        user_id=user.user_id,
        name="Dave",
        phone="+380991234571",
        address="Dnipro, 3",
        status="pending",
        cart_items=cart_items,
    )

    assert order.promo_code is None
    assert order.discount_amount == Decimal("0")


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_user_orders_returns_users_orders():
    user = await make_user_async(user_id=302001, phone="+380991234572")
    product = await make_product_async()
    cart_items = await _create_cart_items(user, product)

    await add_order_with_items(
        user_id=user.user_id, name="X", phone="+380991234572",
        address="A", status="pending", cart_items=cart_items,
    )

    orders = await get_user_orders(user.user_id)
    assert len(orders) >= 1


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_user_orders_empty_for_unknown_user():
    orders = await get_user_orders(999999999)
    assert orders == []


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_order_by_id_returns_order():
    user = await make_user_async(user_id=303001, phone="+380991234573")
    product = await make_product_async()
    cart_items = await _create_cart_items(user, product)

    order = await add_order_with_items(
        user_id=user.user_id, name="Y", phone="+380991234573",
        address="B", status="completed", cart_items=cart_items,
    )

    fetched = await get_order_by_id(str(order.id))
    assert fetched is not None
    assert str(fetched.id) == str(order.id)


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_order_by_id_not_found():
    result = await get_order_by_id(str(uuid.uuid4()))
    assert result is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_total_orders_increases_after_creation():
    before = await total_orders()
    user = await make_user_async(user_id=304001, phone="+380991234574")
    product = await make_product_async()
    cart_items = await _create_cart_items(user, product)
    await add_order_with_items(
        user_id=user.user_id, name="Z", phone="+380991234574",
        address="C", status="pending", cart_items=cart_items,
    )
    after = await total_orders()
    assert after == before + 1