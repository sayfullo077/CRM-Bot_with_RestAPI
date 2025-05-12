from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import WebAppInfo
from utils.button_text import stats_menu_msg, settings_btn_msg, orders_history_btn_msg, order_menu_btn_msg, product_menu_button_msg, category_menu_button_msg, shop_menu_button_msg, shop_main_button_msg, existing_link_btn_txt, user_link_btn_txt, back_btn_text, save_link_btn_txt, start_btn_txt, confirm_msg, start_user_has_shop_btn


class ChooseLanguageCallback(CallbackData, prefix='ikb01'):
    language: str


button = InlineKeyboardBuilder()
button.button(text="🇺🇿 O'zbek tili", callback_data=ChooseLanguageCallback(language="uz"))
button.button(text="🇬🇧 English", callback_data=ChooseLanguageCallback(language="en"))
button.button(text="🇺🇿/🇷🇺  Кирилча", callback_data=ChooseLanguageCallback(language="uk"))
button.button(text="🇷🇺 Русский язык", callback_data=ChooseLanguageCallback(language="ru"))
button.adjust(1)


async def back_button(language):
    btn = InlineKeyboardBuilder()
    texts = back_btn_text.get(language)
    btn.button(text=texts["back"], callback_data="back")
    btn.adjust(1)
    return btn.as_markup()


async def user_start_button(language):
    btn = InlineKeyboardBuilder()
    text = start_btn_txt.get(language)
    btn.button(text="🌐 Shop WebApp", web_app=WebAppInfo(url="https://chatgpt.com/"))
    btn.button(text=text["start_link"], callback_data="start_link")
    btn.adjust(1)
    return btn.as_markup()


async def user_has_shop_button(language):
    btn = InlineKeyboardBuilder()
    texts = start_user_has_shop_btn.get(language)
    btn.button(text=texts["business_menu"], callback_data="business_menu")
    btn.button(text=texts["orders_menu"], callback_data="orders_menu")
    btn.button(text=texts["stats_menu"], callback_data="stats_menu")
    btn.button(text=texts["settings_menu"], callback_data="settings_menu")
    btn.adjust(2)
    return btn.as_markup()


async def shop_main_button(language):
    btn = InlineKeyboardBuilder()
    texts = shop_main_button_msg.get(language)
    btn.button(text=texts["shop_menu"], callback_data="shop_menu")
    btn.button(text=texts["category_menu"], callback_data="category_menu")
    btn.button(text=texts["back"], callback_data="back")
    btn.button(text=texts["product_menu"], callback_data="product_menu")
    btn.adjust(2)
    return btn.as_markup()


async def shop_menu_button(language):
    btn = InlineKeyboardBuilder()
    texts = shop_menu_button_msg.get(language)
    btn.button(text=texts["add_shop"], callback_data="start_link")
    btn.button(text=texts["shop_list"], callback_data="shop_list")
    btn.button(text=texts["shop_edit"], callback_data="shop_edit")
    btn.button(text=texts["shop_delete"], callback_data="shop_delete")
    btn.button(text=texts["back"], callback_data="back")
    btn.adjust(1)
    return btn.as_markup()


async def stats_menu_button(language):
    btn = InlineKeyboardBuilder()
    texts = stats_menu_msg.get(language)
    btn.button(text=texts["monthly_summary"], callback_data="monthly_summary")
    btn.button(text=texts["top_products"], callback_data="top_products")
    btn.button(text=texts["back"], callback_data="back")
    btn.button(text=texts["top_customers"], callback_data="top_customers")
    btn.adjust(2)
    return btn.as_markup()


async def settings_button(language, notification):
    btn = InlineKeyboardBuilder()
    texts = settings_btn_msg.get(language)
    btn.button(text=texts["update_language"], callback_data="update_language")
    btn.button(text=texts["update_phone"], callback_data="update_phone")
    btn.button(text=texts["feedback"], callback_data="feedback")
    btn.button(text=texts["about_us"], callback_data="about_us")
    btn.button(text=texts["back"], callback_data="back")
    if notification:
        btn.button(text=texts["notification_on"], callback_data="notification_on")
    else:
        btn.button(text=texts["notification_off"], callback_data="notification_off")
    btn.adjust(2)
    return btn.as_markup()


async def category_menu_button(language):
    btn = InlineKeyboardBuilder()
    texts = category_menu_button_msg.get(language)
    btn.button(text=texts["add_category"], callback_data="add_category")
    btn.button(text=texts["category_list"], callback_data="category_list")
    btn.button(text=texts["category_edit"], callback_data="category_edit")
    btn.button(text=texts["category_delete"], callback_data="category_delete")
    btn.button(text=texts["back"], callback_data="back")
    btn.adjust(1)
    return btn.as_markup()


async def product_menu_button(language):
    btn = InlineKeyboardBuilder()
    texts = product_menu_button_msg.get(language)
    btn.button(text=texts["add_product"], callback_data="add_category")
    btn.button(text=texts["product_list"], callback_data="category_list")
    btn.button(text=texts["product_edit"], callback_data="category_edit")
    btn.button(text=texts["product_delete"], callback_data="category_delete")
    btn.button(text=texts["back"], callback_data="back")
    btn.adjust(1)
    return btn.as_markup()


async def order_menu_button(language):
    btn = InlineKeyboardBuilder()
    texts = order_menu_btn_msg.get(language)
    btn.button(text=texts["order_history"], callback_data="order_history")
    btn.button(text=texts["orders_in_process"], callback_data="orders_in_process")
    btn.button(text=texts["back"], callback_data="back")
    btn.button(text=texts["banned_users"], callback_data="banned_users")
    btn.adjust(2)
    return btn.as_markup()


async def orders_history_button(language):
    btn = InlineKeyboardBuilder()
    texts = orders_history_btn_msg.get(language)
    btn.button(text=texts["today_orders"], callback_data="today_orders")
    btn.button(text=texts["weekly_orders"], callback_data="weekly_orders")
    btn.button(text=texts["monthly_orders"], callback_data="monthly_orders")
    btn.button(text=texts["all_orders"], callback_data="all_orders")
    btn.button(text=texts["back"], callback_data="back")
    btn.adjust(2, 2, 1)
    return btn.as_markup()


async def user_link_button(language):
    btn = InlineKeyboardBuilder()
    texts = user_link_btn_txt.get(language)
    btn.button(text=texts["update_link"], callback_data="update_link")
    btn.button(text=texts["save_link"], callback_data="save_link")
    btn.button(text=texts["back"], callback_data="back")
    btn.adjust(1)
    return btn.as_markup()


async def user_existing_link_button(language):
    btn = InlineKeyboardBuilder()
    texts = existing_link_btn_txt.get(language, existing_link_btn_txt["uz"])
    btn.button(text=texts["update_link"], callback_data="update_link")
    btn.button(text=texts["admin_panel"], web_app=WebAppInfo(url="https://chatgpt.com/"))
    btn.button(text=texts["admin_panel"], web_app=WebAppInfo(url="https://c71f-188-113-212-176.ngrok-free.app/admin/"))
    btn.button(text=texts["back"], callback_data="back")
    btn.adjust(1)
    return btn.as_markup()


async def save_link_button(language):
    btn = InlineKeyboardBuilder()
    texts = save_link_btn_txt.get(language, save_link_btn_txt["uz"])
    btn.button(text=texts["retry"], callback_data="retry")
    btn.button(text=texts["save_link"], callback_data="save_link")
    btn.adjust(2)
    return btn.as_markup()


async def confirm_button(language):
    btn = InlineKeyboardBuilder()
    texts = confirm_msg.get(language)
    btn.button(text=texts["confirm"], callback_data="confirm")
    btn.button(text=texts["cancel"], callback_data="cancel")
    btn.adjust(2)
    return btn.as_markup()
