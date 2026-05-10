from asgiref.sync import sync_to_async
from django.utils import timezone

from django_project.telegrambot.usersmanage.models import PromoCode


@sync_to_async
def get_all_promo_codes() -> list[PromoCode]:
    return list(PromoCode.objects.order_by("-created_at"))


@sync_to_async
def get_promo_by_id(promo_id: int) -> PromoCode | None:
    try:
        return PromoCode.objects.get(id=promo_id)
    except PromoCode.DoesNotExist:
        return None


@sync_to_async
def create_promo_code(data: dict) -> PromoCode:
    return PromoCode.objects.create(**data)


@sync_to_async
def update_promo_code(promo_id: int, data: dict) -> None:
    PromoCode.objects.filter(id=promo_id).update(**data)


@sync_to_async
def delete_promo_code_by_id(promo_id: int) -> None:
    PromoCode.objects.filter(id=promo_id).delete()


@sync_to_async
def toggle_promo_active(promo_id: int) -> bool:
    promo = PromoCode.objects.filter(id=promo_id).first()
    if promo:
        promo.is_active = not promo.is_active
        promo.save(update_fields=["is_active"])
        return promo.is_active
    return False


@sync_to_async
def validate_promo_code(code: str) -> tuple[PromoCode | None, str | None]:
    """
    Returns (promo, error_key). error_key is None when the code is valid.
    Possible error keys: not_found, inactive, not_started, expired, limit_reached.
    """
    try:
        promo = PromoCode.objects.get(code__iexact=code)
    except PromoCode.DoesNotExist:
        return None, "not_found"

    now = timezone.now()
    if not promo.is_active:
        return promo, "inactive"
    if now < promo.valid_from:
        return promo, "not_started"
    if now > promo.valid_until:
        return promo, "expired"
    if promo.max_uses is not None and promo.current_uses >= promo.max_uses:
        return promo, "limit_reached"

    return promo, None