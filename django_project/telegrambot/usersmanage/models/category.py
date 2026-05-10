from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel
from django.utils.translation import gettext_lazy as _


class Category(TranslatableModel, TimeBasedModel):
    id = models.AutoField(primary_key=True)
    translations = TranslatedFields(name=models.CharField(max_length=150, help_text=_("Name of the category")))

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _("Category")

    def __str__(self):
        return f"{self.name}"