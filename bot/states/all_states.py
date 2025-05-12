from aiogram.filters.state import State, StatesGroup


class MeniMenuState(StatesGroup):
    main_menu = State()
    static_menu = State()


class UserAdd(StatesGroup):
    start = State()
    language = State()
    phone = State()
    link = State()
    update_link = State()
    check_link = State()
    save_link = State()


class ShopAdd(StatesGroup):
    title = State()
    desc = State()
    image = State()
    check = State()


class CategoryAdd(StatesGroup):
    title = State()
    desc = State()
    image = State()
    check = State()


class ProductAdd(StatesGroup):
    title = State()
    desc = State()
    image = State()
    price = State()
    check = State()


class ShopState(StatesGroup):
    mein_menu = State()
    shop_menu = State()
    category_menu = State()
    subcategory = State()
    product_menu = State()
    info = State()


class OrderState(StatesGroup):
    order_menu = State()
    order_history = State()