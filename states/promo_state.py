from aiogram.fsm.state import State, StatesGroup


class AddPromoCode(StatesGroup):
    code = State()
    discount_percent = State()
    valid_from = State()
    valid_until = State()
    max_uses = State()

    promo_for_change = None