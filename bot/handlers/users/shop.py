from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from aiohttp import ClientSession
from aiogram.filters import or_f

from states.all_states import UserAdd, ShopAdd, ShopState
from utils.api import create_shop, get_user
from utils.dictionary_words import select_menu_msg, name_length_error_msg, desc_length_error_msg, take_title_msg, invalid_image_format_msg, only_image_allowed_msg, take_description_msg
from keyboards.inline.inline_buttons import back_button, confirm_button, user_start_button, shop_main_button, shop_menu_button
from loader import dp, bot


@dp.callback_query(F.data.startswith("business_menu"), UserAdd.start)
async def business_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ShopState.mein_menu)
    telegram_id = call.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        shop_main_btn = await shop_main_button(language)
        await call.message.edit_text(text=select_menu_msg.get(language), reply_markup=shop_main_btn)


@dp.callback_query(F.data.startswith("shop_menu"), ShopState.mein_menu)
async def shop_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ShopState.shop_menu)
    telegram_id = call.from_user.id
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        shop_menu_btn = await shop_menu_button(language)
        await call.message.edit_text(text=select_menu_msg.get(language), reply_markup=shop_menu_btn)


#####<<create_shop>>#####
@dp.message(UserAdd.save_link)
async def get_shop_title(message: types.Message, state: FSMContext):
    title = message.text
    data = await state.get_data()
    language = data.get('language')
    back_btn = await back_button(language)
    if not (5 <= len(title) <= 50):
        await message.answer(
            text=name_length_error_msg.get(language)
        )
        return
    await state.update_data(title=title)
    await message.answer(text=take_title_msg.get(language), reply_markup=back_btn)
    await state.set_state(ShopAdd.title)


@dp.message(ShopAdd.title)
async def get_shop_desc(message: types.Message, state: FSMContext):
    desc = message.text
    data = await state.get_data()
    language = data.get('language')
    back_btn = await back_button(language)
    if not (5 <= len(desc) <= 100):
        await message.answer(
            text=desc_length_error_msg.get(language)
        )
        return
    await state.update_data(desc=desc)
    await message.answer(text=take_description_msg.get(language), reply_markup=back_btn)
    await state.set_state(ShopAdd.image)


@dp.message(ShopAdd.image, F.content_type == ContentType.PHOTO)
async def get_shop_image(message: types.Message, state: FSMContext):
    image = message.photo[-1]
    data = await state.get_data()
    language = data.get('language')
    back_btn = await back_button(language)
    telegram_id = message.from_user.id
    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
    else:
        await message.answer(text=only_image_allowed_msg.get(language), reply_markup=back_btn)
        return

    file_info = await bot.get_file(image.file_id)
    file_extension = file_info.file_path.split(".")[-1].lower()
    valid_extensions = ["jpg", "jpeg", "png", "webp"]

    if file_extension not in valid_extensions:
        await message.answer(text=invalid_image_format_msg.get(language))
        return
    text = f"🛍 Kiritilgan ma'lumotlar to'g'rimi?\n\n" \
           f"📌 Nomi: {data.get('title')}\n\n"\
           f"📋 Qo'shimcha ma'lumoti: {data.get('desc')}\n\n" \
           f"🔗 Linki: {data.get('telegram_link')}\n\n"
    await message.delete()
    reply_markup = await confirm_button(language)
    await bot.send_photo(
        chat_id=telegram_id,
        photo=image.file_id,
        caption=text,
        reply_markup=reply_markup
    )
    await state.set_state(ShopAdd.check)


@dp.message(ShopAdd.image)
async def image_format_error(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    back_btn = await back_button(language)
    await message.answer(text=only_image_allowed_msg.get(language), reply_markup=back_btn)


@dp.callback_query(F.data.startswith("confirm"), or_f(UserAdd.link, ShopAdd.check))
async def confirm_shop(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    data = await state.get_data()
    title = data.get("title")
    desc = data.get("desc")
    image = data.get("image")
    telegram_link = data.get("telegram_link")
    async with ClientSession() as session:
        user = await get_user(telegram_id=telegram_id, session=session)
        language = user.get("language")
        user_start_btn = await user_start_button(language)
        try:
            await create_shop(telegram_id=telegram_id, title=title, desc=desc, image=image, telegram_link=telegram_link, language=language, session=session)
        except Exception as e:
            await call.message.answer(f"Xatolik bor shop qo'shishda : {e}")
        await call.message.answer(text="Saqlandi !", reply_markup=user_start_btn)


@dp.callback_query(F.data.startwith("cancel"), or_f(ShopAdd.check, UserAdd.link))
async def cancel_shop(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserAdd.start)
    data = await state.get_data()
    langauge = data.get("language")
    user_start_btn = await user_start_button(langauge)
    await call.message.edit_text("Bekor qilindi !", reply_markup=user_start_btn)
