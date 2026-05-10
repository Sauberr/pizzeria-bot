from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel
from django.core.validators import MinValueValidator

class Product(TranslatableModel, TimeBasedModel):
    id = models.AutoField(primary_key=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=150, help_text=_("Name of the product")),
        description=models.TextField(max_length=1024, help_text=_("Description of the product")),
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)], help_text=_("Price of the product"))
    image = models.ImageField(upload_to="products", blank=True, null=True, help_text=_("Image of the product"))
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )

    class Meta:
        verbose_name_plural = _("Products")
        verbose_name = _("Product")

    def __str__(self):
        return f"{self.name}"