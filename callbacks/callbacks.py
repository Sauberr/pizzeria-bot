from aiogram.filters.callback_data import CallbackData


class MenuCallBack(CallbackData, prefix="menu"):
    level: int
    menu_name: str
    category: int | None = None
    page: int = 1
    product_id: int | None = None


class OrderDetailCallBack(CallbackData, prefix="order_detail"):
    order_id: str