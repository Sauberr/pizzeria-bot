from datetime import timedelta
from decimal import Decimal

import pytest
from asgiref.sync import sync_to_async
from django.utils import timezone

from django_project.telegrambot.usersmanage.models import PromoCode
from queries.promo_queries import (create_promo_code, delete_promo_code_by_id,
                                   get_all_promo_codes, get_promo_by_id,
                                   toggle_promo_active, update_promo_code,
                                   validate_promo_code)
from tests.conftest import make_promo_async


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_validate_returns_promo_and_no_error_for_valid_code():
    promo = await make_promo_async(code="VALID10")
    result, error = await validate_promo_code("VALID10")
    assert error is None
    assert result.id == promo.id


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_validate_is_case_insensitive():
    await make_promo_async(code="UPPER")
    result, error = await validate_promo_code("upper")
    assert error is None
    assert result.code == "UPPER"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_validate_not_found():
    result, error = await validate_promo_code("DOESNOTEXIST")
    assert result is None
    assert error == "not_found"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_validate_inactive_code():
    await make_promo_async(code="OFF", is_active=False)
    _, error = await validate_promo_code("OFF")
    assert error == "inactive"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_validate_not_started_code():
    now = timezone.now()

    @sync_to_async
    def _create():
        return PromoCode.objects.create(
            code="FUTURE",
            discount_percent=Decimal("10"),
            valid_from=now + timedelta(days=5),
            valid_until=now + timedelta(days=30),
            max_uses=100,
            is_active=True,
        )

    await _create()
    _, error = await validate_promo_code("FUTURE")
    assert error == "not_started"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_validate_expired_code():
    now = timezone.now()

    @sync_to_async
    def _create():
        return PromoCode.objects.create(
            code="OLDCODE",
            discount_percent=Decimal("10"),
            valid_from=now - timedelta(days=10),
            valid_until=now - timedelta(seconds=1),
            max_uses=100,
            is_active=True,
        )

    await _create()
    _, error = await validate_promo_code("OLDCODE")
    assert error == "expired"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_validate_limit_reached():
    await make_promo_async(code="FULL", max_uses=5, current_uses=5)
    _, error = await validate_promo_code("FULL")
    assert error == "limit_reached"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_validate_unlimited_uses_always_valid():
    await make_promo_async(code="UNLIM", max_uses=0, current_uses=9999)

    @sync_to_async
    def _create():
        return PromoCode.objects.create(
            code="NOLIMIT",
            discount_percent=Decimal("5"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=30),
            max_uses=None,
            current_uses=99999,
            is_active=True,
        )

    await _create()
    _, error = await validate_promo_code("NOLIMIT")
    assert error is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_all_promo_codes_returns_list():
    await make_promo_async(code="A1")
    await make_promo_async(code="B2")
    promos = await get_all_promo_codes()
    codes = [p.code for p in promos]
    assert "A1" in codes
    assert "B2" in codes


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_promo_by_id_found():
    promo = await make_promo_async(code="BYID")
    fetched = await get_promo_by_id(promo.id)
    assert fetched is not None
    assert fetched.code == "BYID"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_get_promo_by_id_not_found():
    result = await get_promo_by_id(999999)
    assert result is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_promo_code_saves_to_db():
    now = timezone.now()
    promo = await create_promo_code({
        "code": "NEW50",
        "discount_percent": Decimal("50"),
        "valid_from": now - timedelta(days=1),
        "valid_until": now + timedelta(days=7),
        "max_uses": 10,
        "is_active": True,
    })
    assert promo.pk is not None
    assert promo.code == "NEW50"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_update_promo_code_changes_discount():
    promo = await make_promo_async(code="UPD", discount=10)
    await update_promo_code(promo.id, {"discount_percent": Decimal("30")})
    updated = await get_promo_by_id(promo.id)
    assert updated.discount_percent == Decimal("30")


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_delete_promo_code_removes_from_db():
    promo = await make_promo_async(code="TODELETE")
    await delete_promo_code_by_id(promo.id)
    result = await get_promo_by_id(promo.id)
    assert result is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_toggle_promo_active_true_to_false():
    promo = await make_promo_async(code="TOGGLE1", is_active=True)
    new_state = await toggle_promo_active(promo.id)
    assert new_state is False
    fetched = await get_promo_by_id(promo.id)
    assert fetched.is_active is False


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_toggle_promo_active_false_to_true():
    promo = await make_promo_async(code="TOGGLE2", is_active=False)
    new_state = await toggle_promo_active(promo.id)
    assert new_state is True