import html
import re
import json
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, F
from loader import dp, redis
from aiogram.filters import or_f
from utils.redis_func import get_user_redis
from utils.api import get_user, create_user, update_language_phone, check_phone_number
from keyboards.inline.inline_buttons import button, user_start_button, ChooseLanguageCallback, user_has_shop_button
from states.all_states import UserAdd
from utils.dictionary_words import start_msg, start_has_shop_msg, langauge_set_msg, phone_set_msg, phone_btn_msg, error_msg_phone, phone_save_msg


def escape_for_telegram(text: str | None) -> str:
    if text is None:
        return ""
    return html.escape(text)


@dp.message(CommandStart())
async def start_bot(message: types.Message, state: FSMContext, command: CommandObject):
    await state.set_state(UserAdd.start)
    args = command.args
    payload = None
    if args:
        try:
            payload = args
            await message.answer(f"📦 Siz maxsus linkdan kirdingiz: {payload}")
        except Exception as e:
            await message.answer("❌ Noto‘g‘ri link formati.")
            print("Payload decode xatoligi:", e)
    telegram_id = message.from_user.id
    fullname = escape_for_telegram(message.from_user.full_name)
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    language = message.from_user.language_code
    username = message.from_user.username
    user_data = await get_user_redis(telegram_id)
    if not user_data:
        print("Datalar: ", user_data, "\nType:", type(user_data), "\nShop:", user_data["shop"])
        shop = user_data["shop"]
        if shop:
            user_start_btn = await user_has_shop_button(language)
            text = start_has_shop_msg.get(language)
            greeting = text["greeting"]
            main_menu = text["main_menu"]
            await message.answer(text=f"{greeting} {fullname}\n\n{main_menu}", reply_markup=user_start_btn)

        else:
            user_start_btn = await user_start_button(language)
            texts = start_msg.get(language)
            greeting = texts["greeting"]
            rules = texts["rules"]
            text = f"{greeting} {fullname}\n{rules}"
            await message.answer(text=text, reply_markup=user_start_btn)
    else:
        async with ClientSession() as session:
            user = await get_user(telegram_id=telegram_id, session=session)
            if user:
                language = user.get("language")
                shop = user.get("shops")
                user_data = {
                    "fullname": fullname,
                    "firstname": firstname,
                    "lastname": lastname,
                    "telegram_id": telegram_id,
                    "language": language,
                    "username": username,
                    "shop": shop
                }
                key = f"user_data:{telegram_id}"
                await redis.set(key, json.dumps(user_data), ex=31536000)
                if shop:
                    user_start_btn = await user_has_shop_button(language)
                    text = start_has_shop_msg.get(language)
                    greeting = text["greeting"]
                    main_menu = text["main_menu"]
                    await message.answer(text=f"{greeting} {fullname}\n\n{main_menu}", reply_markup=user_start_btn)

                else:
                    existing_fullname = user.get("fullname", "Foydalanuvchi")
                    user_start_btn = await user_start_button(language)
                    texts = start_msg.get(language)
                    greeting = texts["greeting"]
                    rules = texts["rules"]
                    text = f"{greeting} {existing_fullname}\n{rules}"
                    await message.answer(text=text, reply_markup=user_start_btn)
            else:
                try:
                    await create_user(telegram_id=telegram_id, username=username, fullname=fullname, firstname=firstname, lastname=lastname, language=language, session=session)
                    await message.answer(
                        f"Assalomu alaykum {fullname}\nBotimizga xush kelibsiz!\nKeling avvaliga xizmat ko'rsatish tilni tanlab olaylik.\n\nTilni tanlang!",
                        reply_markup=button.as_markup()
                    )
                except Exception as e:
                    print(f"Foydalanuvchini qo'shish yoki xabar yuborishda xatolik: {e}")


@dp.callback_query(ChooseLanguageCallback.filter(), UserAdd.start)
async def set_language(call: types.CallbackQuery, state: FSMContext, callback_data: ChooseLanguageCallback):
    await state.set_state(UserAdd.language)
    language = callback_data.language
    await state.update_data(language=language)
    text = phone_btn_msg.get(language)
    keyboard = [
        [
            KeyboardButton(
                text=text,
                request_contact=True
            )
        ]
    ]
    markup_request = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    await call.message.delete()
    lang_msg = langauge_set_msg.get(language)
    await call.answer(text=lang_msg, show_alert=False)
    text = phone_set_msg.get(language)
    await call.message.answer(text=text, reply_markup=markup_request)


def clean_phone_number(phone_number):
    phone_number = re.sub(r'\s+', '', phone_number)
    if phone_number.startswith('998'):
        phone_number = '+998' + phone_number[3:]
    elif not phone_number.startswith('+998'):
        phone_number = '+998' + phone_number
    return phone_number


@dp.message(F.contact | F.text.startswith("+998"), or_f(UserAdd.language, UserAdd.phone))
async def handle_phone_input(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print("Hozirgi state:", current_state)
    await state.set_state(UserAdd.phone)
    telegram_id = message.from_user.id
    data = await state.get_data()
    language = data.get('language')
    start_btn = await user_start_button(language)
    phone_number = (
        message.contact.phone_number if message.contact else message.text.strip()
    )
    phone_number = clean_phone_number(phone_number)
    existing_user = await check_phone_number(phone_number=phone_number)
    text = error_msg_phone.get(language)
    if existing_user:
        await message.answer(text=text["exist_phone"])
        return

    if not re.match(r'^\+998\d{9}$', phone_number):
        await message.answer(text=text["format_error_phone_msg"])
        return

    try:
        update_phone_msg = phone_save_msg.get(language)
        async with ClientSession() as session:
            await update_language_phone(telegram_id=telegram_id, phone_number=phone_number, language=language, session=session)
            await message.answer(
                f"{update_phone_msg}: {phone_number}",
                reply_markup=ReplyKeyboardRemove())
            await message.answer("Botga xush kelibsiz", reply_markup=start_btn)

    except Exception as e:
        print("Error in update_user_phone_number:", e)
        await message.answer(text=text["retry_error_phone_msg"])