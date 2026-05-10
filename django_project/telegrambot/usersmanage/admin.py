from django.contrib import admin
from django.utils.html import format_html
from parler.admin import TranslatableAdmin

from .models import (AdminUser, Banner, CaptchaRecord, Cart, Category, Order,
                     OrderItem, Product, PromoCode, TelegramUser)


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_superuser", "is_active")
    list_display_links = ("username",)


@admin.register(Banner)
class BannerAdmin(TranslatableAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="100";" />'.format(object.image.url))

    list_display = (
        "id",
        "name",
        "thumbnail",
        "description",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    list_display_links = ("name",)


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    list_display_links = ("name",)


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    def thumbnail(self, object):
        if object.image:
            return format_html('<img src="{}" width="40";" />'.format(object.image.url))
        return "No image"

    list_display = (
        "id",
        "name",
        "price",
        "category",
        "thumbnail",
        "description",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "description")
    list_filter = ("category", "created_at", "updated_at")
    list_display_links = ("name",)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "phone_number",
        "user_id",
        "language",
        "created_at",
        "updated_at",
    )
    list_display_links = ("first_name", "phone_number", "user_id", "language")
    search_fields = ("first_name", "phone_number", "user_id")
    list_filter = ("created_at", "updated_at")
    ordering = ("first_name",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "created_at", "updated_at")
    search_fields = ("user__first_name", "product__name")
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("user", "product")


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "name",
        "address",
        "phone",
        "status",
        "promo_code",
        "discount_amount",
        "created_at",
        "updated_at",
    )
    inlines = [OrderItemAdmin]
    search_fields = ("id", "name", "address", "phone", "status")
    list_filter = ("status", "created_at", "updated_at")
    raw_id_fields = ("promo_code",)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "discount_percent",
        "valid_from",
        "valid_until",
        "max_uses",
        "current_uses",
        "is_active",
        "created_at",
    )
    search_fields = ("code",)
    list_filter = ("is_active", "valid_from", "valid_until")
    list_display_links = ("code",)
    list_editable = ("is_active",)
    readonly_fields = ("current_uses", "created_at", "updated_at")


@admin.register(CaptchaRecord)
class CaptchaRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "captcha",
        "timestamp",
        "created_at",
        "updated_at",
        "is_passed",
    )
    search_fields = ("user__first_name", "user__last_name", "captcha")
    list_filter = ("timestamp", "created_at", "updated_at")
    raw_id_fields = ("user",)
