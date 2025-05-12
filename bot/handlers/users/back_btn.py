from aiogram import F, types
from aiogram.filters import or_f
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext

from states.all_states import UserAdd, ShopState, OrderState, MeniMenuState
from utils.api import get_user
from utils.dictionary_words import start_has_shop_msg, start_msg, select_menu_msg
from keyboards.inline.inline_buttons import user_has_shop_button, user_start_button, shop_main_button, order_menu_button
from loader import dp


@dp.callback_query(F.data.startswith("back"), or_f(ShopState.mein_menu, ShopState.shop_menu, ShopState.category_menu, OrderState.order_menu, ShopState.product_menu, OrderState.order_history, MeniMenuState.static_menu))
async def back_button_func(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    print("Hozirgi state:", current_state)
    telegram_id = call.from_user.id

    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        if current_state in [
            ShopState.mein_menu,
            OrderState.order_menu,
            MeniMenuState.static_menu,
            UserAdd.link
        ]:
            await state.set_state(UserAdd.start)
            language = user.get("language")
            shop = user.get("shops")
            if shop:
                user_start_btn = await user_has_shop_button(language)
                text = start_has_shop_msg.get(language)
                main_menu = text["main_menu"]
                await call.message.edit_text(text=f"{main_menu}", reply_markup=user_start_btn)

            else:
                existing_fullname = user.get("fullname", "Foydalanuvchi")
                user_start_btn = await user_start_button(language)
                texts = start_msg.get(language)
                greeting = texts["greeting"]
                rules = texts["rules"]
                text = f"{greeting} {existing_fullname}\n{rules}"
                await call.message.edit_text(text=text, reply_markup=user_start_btn)

        elif current_state in [
            ShopState.shop_menu,
            ShopState.category_menu,
            ShopState.product_menu,

        ]:
            await state.set_state(ShopState.mein_menu)
            shop_mein_btn = await shop_main_button(language)
            await call.message.edit_text(text=select_menu_msg.get(language), reply_markup=shop_mein_btn)

        elif current_state in [
            OrderState.order_history
        ]:
            await state.set_state(OrderState.order_menu)
            telegram_id = call.from_user.id
            async with ClientSession() as session:
                user = await get_user(telegram_id=telegram_id, session=session)
                language = user.get("language")
                shop_main_btn = await order_menu_button(language)
                await call.message.edit_text(text=select_menu_msg.get(language), reply_markup=shop_main_btn)