from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession

from states.all_states import UserAdd, ShopState
from utils.api import get_user
from utils.dictionary_words import select_menu_msg
from keyboards.inline.inline_buttons import settings_button
from loader import dp


@dp.callback_query(F.data.startswith("settings_menu"), UserAdd.start)
async def settings_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ShopState.mein_menu)
    telegram_id = call.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        status = user.get("notification")
        shop_main_btn = await settings_button(language, status)
        await call.message.edit_text(text=select_menu_msg.get(language), reply_markup=shop_main_btn)