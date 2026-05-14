from decimal import Decimal
from typing import Optional

from asgiref.sync import sync_to_async
from django.db.models import Count
from parler.utils.context import switch_language

from django_project.telegrambot.usersmanage.models import Category, Product


@sync_to_async
def add_product(data: dict) -> None:
    product = Product.objects.create(
        price=Decimal(str(data["price"])),
        image=data.get("image"),
        category_id=int(data["category"]),
    )

    ProductTranslation = product.translations.model

    translations = [
        ProductTranslation(
            master=product,
            language_code="en",
            name=data["en_name"],
            description=data["en_description"]
        ),
        ProductTranslation(
            master=product,
            language_code="ru",
            name=data["ru_name"],
            description=data["ru_description"]
        )
    ]
    ProductTranslation.objects.bulk_create(translations)


@sync_to_async
def get_products(category_id: Optional[int] = None) -> list[Product]:
    try:
        qs = Product.objects.prefetch_related("translations")
        if category_id is not None:
            qs = qs.filter(category_id=int(category_id))
        return list(qs)
    except Product.DoesNotExist:
        return []


@sync_to_async
def get_product(product_id: int) -> Optional[Product]:
    return Product.objects.filter(id=product_id).first()


@sync_to_async
def update_product(product_id: int, data: dict) -> None:
    product = Product.objects.get(id=product_id)

    product.price = Decimal(str(data["price"]))
    if "image" in data:
        product.image = data["image"]
    product.category_id = int(data["category"])
    product.save()

    ProductTranslation = product.translations.model

    if "en_name" in data or "en_description" in data:
        en_trans, created = ProductTranslation.objects.get_or_create(
            master=product,
            language_code="en",
            defaults={"name": data.get("en_name", ""), "description": data.get("en_description", "")},
        )
        if not created:
            if "en_name" in data:
                en_trans.name = data["en_name"]
            if "en_description" in data:
                en_trans.description = data["en_description"]
            en_trans.save()

    if "ru_name" in data or "ru_description" in data:
        ru_trans, created = ProductTranslation.objects.get_or_create(
            master=product,
            language_code="ru",
            defaults={"name": data.get("ru_name", ""), "description": data.get("ru_description", "")},
        )
        if not created:
            if "ru_name" in data:
                ru_trans.name = data["ru_name"]
            if "ru_description" in data:
                ru_trans.description = data["ru_description"]
            ru_trans.save()


@sync_to_async
def delete_product(product_id: int) -> None:
    Product.objects.filter(id=product_id).delete()


@sync_to_async
def total_products() -> int:
    return Product.objects.count()


@sync_to_async
def total_products_by_category() -> dict[str, int]:
    return {
        cat.name: cat.product_count
        for cat in Category.objects.annotate(product_count=Count("products"))
    }


@sync_to_async
def get_product_for_edit(product_id: int) -> dict | None:
    try:
        product = Product.objects.prefetch_related("translations").get(id=product_id)
        result: dict = {
            "id": product.id,
            "price": str(product.price),
            "image_name": product.image.name if product.image else None,
            "image_path": str(product.image.path) if product.image else None,
        }
        for lang in ("en", "ru"):
            with switch_language(product, lang):
                result[f"name_{lang}"] = product.name or ""
                result[f"description_{lang}"] = product.description or ""
        return result
    except Product.DoesNotExist:
        return None