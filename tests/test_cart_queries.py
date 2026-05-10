import pytest
from asgiref.sync import sync_to_async

from django_project.telegrambot.usersmanage.models import Cart
from queries.cart_queries import (add_to_cart, clear_cart, delete_from_cart,
                                  get_user_carts, reduce_product_in_cart)
from tests.conftest import make_category_async, make_product_async, make_user_async


async def _count_cart(user_id: int) -> int:
    carts = await get_user_carts(user_id)
    return len(carts)


async def _get_quantity(user_id: int, product_id: int) -> int | None:
    @sync_to_async
    def _fetch():
        item = Cart.objects.filter(user__user_id=user_id, product_id=product_id).first()
        return item.quantity if item else None

    return await _fetch()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_add_to_cart_creates_new_item():
    user = await make_user_async(user_id=401001)
    product = await make_product_async()

    await add_to_cart(user.user_id, product.id)

    assert await _count_cart(user.user_id) == 1


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_add_to_cart_increments_quantity_on_duplicate():
    user = await make_user_async(user_id=401002, phone="+380992223345")
    product = await make_product_async()

    await add_to_cart(user.user_id, product.id)
    await add_to_cart(user.user_id, product.id)

    assert await _count_cart(user.user_id) == 1
    assert await _get_quantity(user.user_id, product.id) == 2


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_add_to_cart_multiple_products():
    user = await make_user_async(user_id=401003, phone="+380992223346")
    cat = await make_category_async("Drinks")
    p1 = await make_product_async(category=cat)
    p2 = await make_product_async(price="5.00", category=cat)

    await add_to_cart(user.user_id, p1.id)
    await add_to_cart(user.user_id, p2.id)

    assert await _count_cart(user.user_id) == 2

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_reduce_decrements_quantity():
    user = await make_user_async(user_id=402001, phone="+380992223347")
    product = await make_product_async()

    await add_to_cart(user.user_id, product.id)
    await add_to_cart(user.user_id, product.id)
    await reduce_product_in_cart(user.user_id, product.id)

    assert await _get_quantity(user.user_id, product.id) == 1


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_reduce_removes_item_when_quantity_hits_zero():
    user = await make_user_async(user_id=402002, phone="+380992223348")
    product = await make_product_async()

    await add_to_cart(user.user_id, product.id)
    await reduce_product_in_cart(user.user_id, product.id)

    assert await _count_cart(user.user_id) == 0


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_reduce_returns_false_when_item_removed():
    user = await make_user_async(user_id=402003, phone="+380992223349")
    product = await make_product_async()

    await add_to_cart(user.user_id, product.id)
    still_exists = await reduce_product_in_cart(user.user_id, product.id)

    assert still_exists is False


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_reduce_returns_true_when_item_still_exists():
    user = await make_user_async(user_id=402004, phone="+380992223350")
    product = await make_product_async()

    await add_to_cart(user.user_id, product.id)
    await add_to_cart(user.user_id, product.id)
    still_exists = await reduce_product_in_cart(user.user_id, product.id)

    assert still_exists is True

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_delete_from_cart_removes_item():
    user = await make_user_async(user_id=403001, phone="+380992223351")
    product = await make_product_async()

    await add_to_cart(user.user_id, product.id)
    await delete_from_cart(user.user_id, product.id)

    assert await _count_cart(user.user_id) == 0


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_delete_from_cart_only_removes_target_product():
    user = await make_user_async(user_id=403002, phone="+380992223352")
    cat = await make_category_async("Sauces")
    p1 = await make_product_async(category=cat)
    p2 = await make_product_async(price="3.00", category=cat)

    await add_to_cart(user.user_id, p1.id)
    await add_to_cart(user.user_id, p2.id)
    await delete_from_cart(user.user_id, p1.id)

    assert await _count_cart(user.user_id) == 1
    assert await _get_quantity(user.user_id, p2.id) == 1


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_clear_cart_removes_all_items():
    user = await make_user_async(user_id=404001, phone="+380992223353")
    cat = await make_category_async("Desserts")
    p1 = await make_product_async(category=cat)
    p2 = await make_product_async(price="6.00", category=cat)

    await add_to_cart(user.user_id, p1.id)
    await add_to_cart(user.user_id, p2.id)
    await clear_cart(user.user_id)

    assert await _count_cart(user.user_id) == 0


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_clear_cart_does_not_affect_other_users():
    u1 = await make_user_async(user_id=404002, phone="+380992223354")
    u2 = await make_user_async(user_id=404003, phone="+380992223355")
    product = await make_product_async()

    await add_to_cart(u1.user_id, product.id)
    await add_to_cart(u2.user_id, product.id)
    await clear_cart(u1.user_id)

    assert await _count_cart(u1.user_id) == 0
    assert await _count_cart(u2.user_id) == 1


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_user_carts_empty_for_new_user():
    user = await make_user_async(user_id=405001, phone="+380992223356")
    carts = await get_user_carts(user.user_id)
    assert carts == []