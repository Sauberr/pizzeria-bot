from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from callbacks.callbacks import MenuCallBack, OrderDetailCallBack



def get_order_details_keyboard(orders, i18n):
    keyboard = []
    for order in orders:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=i18n.order_detail_button(order_id=str(order.id)[:8]),
                    callback_data=OrderDetailCallBack(order_id=str(order.id)).pack(),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=i18n.back_button(),
                callback_data=MenuCallBack(menu_name="main", level=0).pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)