from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from aiohttp import ClientSession
from aiogram.filters import or_f

from states.all_states import ShopState
from utils.api import get_user
from utils.dictionary_words import select_menu_msg
from keyboards.inline.inline_buttons import back_button, product_menu_button
from loader import dp


@dp.callback_query(F.data.startswith("product_menu"), ShopState.mein_menu)
async def shop_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ShopState.product_menu)
    telegram_id = call.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        shop_menu_btn = await product_menu_button(language)
        await call.message.edit_text(text=select_menu_msg.get(language), reply_markup=shop_menu_btn)