import random
import string
import re
import json

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession

from loader import dp, bot, redis
from utils.api import get_user, check_link_exist, update_telegram_link
from states.all_states import UserAdd, ShopState
from aiogram.utils.deep_linking import create_start_link
from keyboards.inline.inline_buttons import user_link_button, user_existing_link_button, back_button, save_link_button
from utils.dictionary_words import update_link_func_text, start_business_text, error_link_text, error_link_format_text, new_link_msg, error_link_size_msg, take_link_msg, update_link_msg


def generate_unique_code(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


@dp.callback_query(F.data.startswith("start_link"))
async def get_link(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    telegram_id = callback_query.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        shops = user.get("shops")
        existing_link = user.get("link")
        fullname = user.get("fullname")
        firstname = user.get("firstname")
        lastname = user.get("lastname")
        username = user.get("username")
        language = user.get("language")
        user_data = {
            "fullname": fullname,
            "firstname": firstname,
            "lastname": lastname,
            "telegram_id": telegram_id,
            "language": language,
            "username": username
        }
        key = f"user_data:{telegram_id}"
        await redis.set(key, json.dumps(user_data), ex=31536000)
        await state.update_data(language=language)
        if current_state == ShopState.shop_menu:
            unique_code = generate_unique_code()
            telegram_link = await create_start_link(bot, f'{unique_code}', encode=False)
            await state.update_data(telegram_link=telegram_link)
            user_link_btn = await user_link_button(language)
            text = start_business_text.get(language)
            text += telegram_link
            await callback_query.message.edit_text(text=text, reply_markup=user_link_btn)
        elif shops:
            await state.update_data(existing_link=existing_link)
            user_existing_link_btn = await user_existing_link_button(language)
            await callback_query.message.edit_text(text="Link bor", reply_markup=user_existing_link_btn)
        else:
            unique_code = generate_unique_code()
            telegram_link = await create_start_link(bot, f'{unique_code}', encode=False)
            await state.update_data(telegram_link=telegram_link)
            user_link_btn = await user_link_button(language)
            text = start_business_text.get(language)
            text += telegram_link
            await callback_query.message.edit_text(text=text, reply_markup=user_link_btn)
        await state.set_state(UserAdd.link)


@dp.callback_query(F.data.startswith("update_link"), UserAdd.link)
async def update_link_func(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserAdd.update_link)
    telegram_id = callback_query.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        await state.update_data(language=language)
        back_btn = await back_button(language)
        data = await state.get_data()
        telegram_link = data.get('telegram_link')
        existing_link = data.get('existing_link')
        if existing_link:
            select_link = existing_link
            await state.update_data(select_link=select_link)
        else:
            select_link = telegram_link
            await state.update_data(select_link=select_link)
        text = select_link
        text += update_link_func_text.get(language)
        await callback_query.message.edit_text(text=text, reply_markup=back_btn)


def clean_link(link: str) -> str:
    if not isinstance(link, str):
        link = str(link)
    link = re.sub(r'[^a-zA-Z0-9_-]', '', link)
    link = link.lower()
    return link


@dp.message(UserAdd.update_link)
async def check_new_link(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    telegram_link = message.text
    telegram_link = clean_link(telegram_link)
    save_link_btn = await save_link_button(language)
    if not (5 <= len(telegram_link) <= 20):
        await message.answer(
            text=error_link_size_msg.get(language)
        )
        return

    if not re.sub(r'[^a-zA-Z0-9_-]', '', telegram_link):
        await message.answer(
            text=error_link_format_text.get(language)
        )
        return

    telegram_link = await create_start_link(bot, f'{telegram_link}', encode=False)
    check_link = await check_link_exist(telegram_link)

    if check_link:
        text = error_link_text.get(language)
        await message.answer(text=text)
        return
    text = telegram_link
    text += new_link_msg.get(language)
    await message.answer(text=text, reply_markup=save_link_btn)
    await state.set_state(UserAdd.check_link)


@dp.callback_query(F.data.startswith("retry"), UserAdd.check_link)
async def update_link_func(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserAdd.update_link)
    telegram_id = callback_query.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        back_btn = await back_button(language)
        data = await state.get_data()
        telegram_link = data.get('telegram_link')
        existing_link = data.get('existing_link')
        if existing_link:
            select_link = existing_link
            await state.update_data(select_link=select_link)
        else:
            select_link = telegram_link
            await state.update_data(select_link=select_link)
        text = select_link
        text += update_link_func_text.get(language)
        await state.update_data(language=language)
        await callback_query.message.edit_text(text=text, reply_markup=back_btn)


@dp.callback_query(F.data.startswith("save_link"))
async def save_user_link(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserAdd.save_link)
    telegram_id = call.from_user.id
    data = await state.get_data()
    telegram_link = data.get('telegram_link')
    existing_link = data.get('existing_link')
    if existing_link:
        select_link = existing_link
    else:
        select_link = telegram_link
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        shops = user.get("shops")
        language = user.get("language")
        if shops:
            text = update_link_msg.get(language)
            await update_telegram_link(telegram_link=select_link, telegram_id=telegram_id, session=session)
            await call.message.edit_text(text=text)
        else:
            await state.update_data(telegram_link=select_link)
            text = take_link_msg.get(language)
            await call.message.edit_text(text=text)
