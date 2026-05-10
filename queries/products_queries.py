from typing import Optional

from asgiref.sync import sync_to_async
from django.db.models import Count
from django_project.telegrambot.usersmanage.models import Category, Product


@sync_to_async
def add_product(data: dict) -> None:
    product = Product.objects.create(
        price=float(data["price"]),
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
        if category_id is not None:
            products = Product.objects.filter(category_id=int(category_id))
        else:
            products = Product.objects.all()
        return list(products)
    except Product.DoesNotExist:
        return []


@sync_to_async
def get_product(product_id: int) -> Optional[Product]:
    return Product.objects.filter(id=product_id).first()


@sync_to_async
def update_product(product_id: int, data: dict) -> None:
    product = Product.objects.get(id=product_id)

    product.price = float(data["price"])
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