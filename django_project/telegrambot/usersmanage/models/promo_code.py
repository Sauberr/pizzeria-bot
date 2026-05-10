from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_project.telegrambot.usersmanage.models.basemodel import TimeBasedModel


class PromoCode(TimeBasedModel):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Discount %"),
        help_text=_("Discount percentage, e.g. 15 for 15%"),
    )
    valid_from = models.DateTimeField(verbose_name=_("Valid from"))
    valid_until = models.DateTimeField(verbose_name=_("Valid until"))
    max_uses = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Max uses"),
        help_text=_("Leave empty for unlimited uses"),
    )
    current_uses = models.PositiveIntegerField(default=0, verbose_name=_("Current uses"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Promo Code")
        verbose_name_plural = _("Promo Codes")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

    @property
    def is_currently_valid(self) -> bool:
        now = timezone.now()
        return (
            self.is_active
            and self.valid_from <= now <= self.valid_until
            and (self.max_uses is None or self.current_uses < self.max_uses)
        )