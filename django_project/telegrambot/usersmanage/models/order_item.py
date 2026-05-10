from django.db import models
from django.utils.translation import gettext_lazy as _

from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel
from django.core.validators import MinValueValidator


class OrderItem(TimeBasedModel):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.IntegerField(help_text=_("Quantity of the product in the order"))
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)], help_text=_("Price of the product at the time of order"))

    class Meta:
        verbose_name_plural = _("Order Items")
        verbose_name = _("Order Item")

    def __str__(self):
        return (
            f"OrderItem {self.id} - Order {self.order.id} - Product {self.product.name}"
        )
