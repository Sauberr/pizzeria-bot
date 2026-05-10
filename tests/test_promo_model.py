from datetime import timedelta
from decimal import Decimal

import pytest
from django.db import IntegrityError
from django.utils import timezone

from django_project.telegrambot.usersmanage.models import PromoCode


def make_promo(**kwargs):
    now = timezone.now()
    defaults = dict(
        code="CODE",
        discount_percent=Decimal("10.00"),
        valid_from=now - timedelta(days=1),
        valid_until=now + timedelta(days=30),
        max_uses=100,
        current_uses=0,
        is_active=True,
    )
    defaults.update(kwargs)
    return PromoCode(**defaults)


@pytest.mark.django_db
def test_valid_promo_is_currently_valid():
    assert make_promo().is_currently_valid is True


@pytest.mark.django_db
def test_inactive_promo_is_not_valid():
    assert make_promo(is_active=False).is_currently_valid is False


@pytest.mark.django_db
def test_not_started_promo_is_not_valid():
    now = timezone.now()
    promo = make_promo(
        valid_from=now + timedelta(days=1),
        valid_until=now + timedelta(days=30),
    )
    assert promo.is_currently_valid is False


@pytest.mark.django_db
def test_expired_promo_is_not_valid():
    now = timezone.now()
    promo = make_promo(
        valid_from=now - timedelta(days=10),
        valid_until=now - timedelta(seconds=1),
    )
    assert promo.is_currently_valid is False


@pytest.mark.django_db
def test_promo_at_usage_limit_is_not_valid():
    promo = make_promo(max_uses=5, current_uses=5)
    assert promo.is_currently_valid is False


@pytest.mark.django_db
def test_promo_below_usage_limit_is_valid():
    promo = make_promo(max_uses=10, current_uses=9)
    assert promo.is_currently_valid is True


@pytest.mark.django_db
def test_unlimited_promo_is_valid_regardless_of_uses():
    promo = make_promo(max_uses=None, current_uses=99999)
    assert promo.is_currently_valid is True


@pytest.mark.django_db
def test_inactive_and_expired_promo_is_not_valid():
    now = timezone.now()
    promo = make_promo(
        is_active=False,
        valid_until=now - timedelta(days=1),
    )
    assert promo.is_currently_valid is False


@pytest.mark.django_db
def test_promo_str_contains_code_and_percent():
    promo = make_promo(code="SUMMER25", discount_percent=Decimal("25.00"))
    assert "SUMMER25" in str(promo)
    assert "25" in str(promo)


@pytest.mark.django_db
def test_promo_saves_and_retrieves_correctly(active_promo):
    fetched = PromoCode.objects.get(code=active_promo.code)
    assert fetched.discount_percent == active_promo.discount_percent
    assert fetched.is_active is True


@pytest.mark.django_db
def test_promo_code_is_unique(active_promo):
    with pytest.raises(IntegrityError):
        PromoCode.objects.create(
            code=active_promo.code,
            discount_percent=Decimal("5.00"),
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(days=1),
        )