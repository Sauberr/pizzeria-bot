from django.db import models
from parler.models import TranslatableModel, TranslatedFields

from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel
from django.utils.translation import gettext_lazy as _


class Banner(TranslatableModel, TimeBasedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, unique=True, help_text=_("Unique name for the banner"))
    image = models.ImageField(upload_to="banners", blank=True, null=True, help_text=_("Image for the banner"))
    translations = TranslatedFields(
        description=models.TextField(max_length=1024, blank=True, null=True, help_text=_("Description of the banner"))
    )

    class Meta:
        verbose_name_plural = _("Banners")
        verbose_name = _("Banner")

    def __str__(self):
        return f"Banner {self.name}"