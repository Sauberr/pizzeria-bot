from decimal import Decimal

from asgiref.sync import sync_to_async
from django.db import transaction, models as db_models

from django_project.telegrambot.usersmanage.models import (Cart, Order,
                                                           OrderItem,
                                                           PromoCode,
                                                           TelegramUser)


@sync_to_async
def get_user_orders(user_id: int) -> list[Order]:
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        return list(Order.objects.filter(user=user).order_by("-created_at"))
    except TelegramUser.DoesNotExist:
        return []


@sync_to_async
def add_order(
    user_id: int, name: str, phone: str, address: str, status: str = "pending"
) -> Order | None:
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        order = Order.objects.create(
            user=user, name=name, phone=phone, address=address, status=status
        )
        return order
    except TelegramUser.DoesNotExist:
        return None


@sync_to_async
def add_order_with_items(
    user_id: int,
    name: str,
    phone: str,
    address: str,
    status: str,
    cart_items: list[Cart],
    promo_code_id: int | None = None,
    discount_amount: float = 0,
) -> Order:
    with transaction.atomic():
        user = TelegramUser.objects.get(user_id=user_id)

        promo = None
        if promo_code_id:
            promo = PromoCode.objects.select_for_update().get(id=promo_code_id)

        order = Order.objects.create(
            user=user,
            name=name,
            phone=phone,
            address=address,
            status=status,
            promo_code=promo,
            discount_amount=Decimal(str(discount_amount)),
        )
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )

        if promo:
            PromoCode.objects.filter(id=promo_code_id).update(
                current_uses=db_models.F("current_uses") + 1
            )

        return order


@sync_to_async
def get_order_by_id(order_id: str) -> Order | None:
    return Order.objects.filter(id=order_id).first()


@sync_to_async
def get_order_items(order_id: str) -> list[OrderItem]:
    items = list(
        OrderItem.objects.filter(order_id=order_id).select_related("product").all()
    )
    return items


@sync_to_async
def total_orders() -> int:
    return Order.objects.count()


@sync_to_async
def get_order_status(order_id: str) -> str:
    try:
        order = Order.objects.get(id=order_id)
        return order.status
    except Order.DoesNotExist:
        return "unknown"
