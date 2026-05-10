from django.db import models
from django.utils.translation import gettext_lazy as _

from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel


class Cart(TimeBasedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        "TelegramUser", on_delete=models.CASCADE, related_name="cart"
    )
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField(help_text=_("Quantity of the product in the cart"))

    class Meta:
        verbose_name_plural = _("Carts")
        verbose_name = _("Cart")

    def __str__(self):
        return f"<Cart {self.user_id} {self.product_id}>"