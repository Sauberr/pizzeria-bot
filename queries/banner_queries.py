from typing import Optional

from asgiref.sync import sync_to_async

from django_project.telegrambot.usersmanage.models import Banner


@sync_to_async
def add_banner_description(data: dict) -> None:
    if not Banner.objects.exists():
        banners = [
            Banner(name=name, description=description)
            for name, description in data.items()
        ]
        Banner.objects.bulk_create(banners)


@sync_to_async
def change_banner_image(name: str, image: str) -> int:
    return Banner.objects.filter(name=name).update(image=image)


@sync_to_async
def get_banner(page: str, user_language: str = "en") -> Optional[Banner]:
    banner = Banner.objects.language(user_language).filter(name=page).first()
    return banner or Banner.objects.filter(name=page).first()


@sync_to_async
def get_info_pages() -> list[Banner]:
    return list(Banner.objects.all())
