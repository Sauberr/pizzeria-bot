from datetime import timedelta
from decimal import Decimal

import pytest
from asgiref.sync import sync_to_async
from django_project.telegrambot.usersmanage.models import PromoCode
from django.utils import timezone




@pytest.fixture
def tg_user(db):
    from django_project.telegrambot.usersmanage.models import TelegramUser
    return TelegramUser.objects.create(
        user_id=100001,
        first_name="TestUser",
        phone_number="+380991112233",
    )


@pytest.fixture
def category(db):
    from django_project.telegrambot.usersmanage.models import Category
    cat = Category()
    cat.set_current_language("en")
    cat.name = "Pizza"
    cat.save()
    return cat


@pytest.fixture
def product(db, category):
    from django_project.telegrambot.usersmanage.models import Product
    p = Product(price=Decimal("12.50"), category=category)
    p.set_current_language("en")
    p.name = "Margherita"
    p.description = "Classic pizza"
    p.save()
    return p


@pytest.fixture
def active_promo(db):
    return _sync_make_promo(code="ACTIVE10", discount=10)


@pytest.fixture
def expired_promo(db):
    now = timezone.now()
    return _sync_make_promo(
        code="EXPIRED",
        discount=5,
        valid_from=now - timedelta(days=30),
        valid_until=now - timedelta(days=1),
    )


def _sync_make_promo(
    code="PROMO",
    discount=15,
    valid_from=None,
    valid_until=None,
    max_uses=100,
    current_uses=0,
    is_active=True,
):
    now = timezone.now()
    return PromoCode.objects.create(
        code=code,
        discount_percent=Decimal(str(discount)),
        valid_from=valid_from or now - timedelta(days=1),
        valid_until=valid_until or now + timedelta(days=30),
        max_uses=max_uses,
        current_uses=current_uses,
        is_active=is_active,
    )


async def make_user_async(user_id=200001, phone="+380992223344"):
    from django_project.telegrambot.usersmanage.models import TelegramUser

    @sync_to_async
    def _create():
        return TelegramUser.objects.create(
            user_id=user_id,
            first_name="Async User",
            phone_number=phone,
        )

    return await _create()


async def make_category_async(name="Burgers"):
    from django_project.telegrambot.usersmanage.models import Category

    @sync_to_async
    def _create():
        cat = Category()
        cat.set_current_language("en")
        cat.name = name
        cat.save()
        return cat

    return await _create()


async def make_product_async(price="15.00", category=None):
    from django_project.telegrambot.usersmanage.models import Product

    if category is None:
        category = await make_category_async()

    @sync_to_async
    def _create():
        p = Product(price=Decimal(price), category=category)
        p.set_current_language("en")
        p.name = "Test Product"
        p.description = "Test description"
        p.save()
        return p

    return await _create()


async def make_promo_async(
    code="ASYNCPROMO",
    discount=20,
    max_uses=50,
    days_valid=30,
    is_active=True,
    current_uses=0,
):
    @sync_to_async
    def _create():
        return _sync_make_promo(
            code=code,
            discount=discount,
            max_uses=max_uses,
            current_uses=current_uses,
            is_active=is_active,
            valid_until=timezone.now() + timedelta(days=days_valid),
        )

    return await _create()