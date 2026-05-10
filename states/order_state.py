from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    name = State()
    phone = State()
    address = State()
    promo_code = State()
    payment = State()
    confirm = State()
