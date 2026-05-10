import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel

ORDER_STATUS = (
    ("pending", "pending"),
    ("completed", "completed"),
    ("cancelled", "cancelled"),
)


class Order(TimeBasedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "TelegramUser", on_delete=models.CASCADE, related_name="orders"
    )
    name = models.CharField(max_length=150, help_text=_("Name of the recipient"))
    address = models.TextField(help_text=_("Delivery address"))
    phone = PhoneNumberField(help_text=_("Contact phone number"))
    status = models.CharField(max_length=25, choices=ORDER_STATUS, default="pending", help_text=_("Status of the order"))
    promo_code = models.ForeignKey(
        "PromoCode",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name=_("Promo code"),
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name=_("Discount amount (USD)")
    )

    class Meta:
        verbose_name_plural = _("Orders")
        verbose_name = _("Order")

    def __str__(self):
        return f"Order {self.id}"