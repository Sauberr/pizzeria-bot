from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel



class CaptchaRecord(TimeBasedModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        "TelegramUser", on_delete=models.CASCADE, related_name="captcha"
    )
    captcha = models.CharField(max_length=50, help_text=_("Captcha value"))
    timestamp = models.DateTimeField(default=timezone.now, help_text=_("Timestamp of the captcha attempt"))
    is_passed = models.BooleanField(default=False, help_text=_("Indicates if the captcha was passed"))

    class Meta:
        verbose_name_plural = _("Captcha")
        verbose_name = _("Captcha")

    def __str__(self):
        return f"Captcha {self.id} - User {self.user.id}"
