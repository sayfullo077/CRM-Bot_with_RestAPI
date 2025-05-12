from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from aiohttp import ClientSession
from aiogram.filters import or_f

from states.all_states import UserAdd, OrderState
from utils.api import create_shop, get_user
from utils.dictionary_words import select_menu_msg
from keyboards.inline.inline_buttons import order_menu_button, orders_history_button
from loader import dp


@dp.callback_query(F.data.startswith("orders_menu"), UserAdd.start)
async def orders_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.order_menu)
    telegram_id = call.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        shop_main_btn = await order_menu_button(language)
        await call.message.edit_text(text=select_menu_msg.get(language), reply_markup=shop_main_btn)


@dp.callback_query(F.data.startswith("order_history"), OrderState.order_menu)
async def orders_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.order_history)
    telegram_id = call.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        shop_main_btn = await orders_history_button(language)
        await call.message.edit_text(text=select_menu_msg.get(language), reply_markup=shop_main_btn)