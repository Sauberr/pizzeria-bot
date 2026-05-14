from aiogram.fsm.state import State, StatesGroup


class AddProduct(StatesGroup):
    en_name: str = State()
    ru_name: str = State()
    en_description: str = State()
    ru_description: str = State()
    category: str = State()
    price: float = State()
    image = State()

    texts = {
        "AddProduct:en_name": "Enter the English name of the product you want to add:",
        "AddProduct:ru_name": "Enter the Russian name of the product you want to add:",
        "AddProduct:en_description": "Enter the English description of the product:",
        "AddProduct:ru_description": "Enter the Russian description of the product:",
        "AddProduct:category": "Enter the category of the product again:",
        "AddProduct:price": "Enter the price of the product again:",
        "AddProduct:image": "Load the image of the product again:",
    }
