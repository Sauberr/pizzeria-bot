from django.contrib import admin
from django.utils.html import format_html

from .models import (AdminUser, Banner, CaptchaRecord, Cart, Category, Order,
                     OrderItem, Product, TelegramUser)


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
class BannerAdmin(admin.ModelAdmin):
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
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    list_display_links = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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
        "created_at",
        "updated_at",
    )
    list_display_links = ("first_name", "phone_number", "user_id")
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
        "created_at",
        "updated_at",
    )
    inlines = [OrderItemAdmin]
    search_fields = ("id", "name", "address", "phone", "status")
    list_filter = ("status", "created_at", "updated_at")


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
