from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel

LANGUAGE = (
    ("en", "English"),
    ("ru", "Russian"),
)


class TelegramUser(TimeBasedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(_("first name"), max_length=30,help_text=_("First name of the user"))
    phone_number = PhoneNumberField(_("phone number"), unique=True, help_text=_("Phone number of the user"))
    language = models.CharField(
        _("language"), max_length=10, choices=LANGUAGE, default="en", help_text=_("Preferred language of the user")
    )

    class Meta:
        verbose_name = _("Telegram User")
        verbose_name_plural = _("Telegram Users")
        ordering = ("first_name",)
        indexes = [
            models.Index(fields=["first_name", "phone_number"]),
        ]

    def __str__(self):
        return f"{self.first_name}".strip()