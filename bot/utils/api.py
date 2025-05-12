import aiohttp
import time

from data.config import BASE_URL, HMAC_SECRET_KEY
from utils.hmac_outh import generate_signature


async def create_user(telegram_id: int, username: str, fullname: str, firstname: str, lastname: str, language: str, session: aiohttp.ClientSession):
    url = f"{BASE_URL}/account/users/add/"
    payload = {
        'telegram_id': telegram_id,
        'username': username,
        'fullname': fullname,
        'firstname': firstname,
        'lastname': lastname,
        'language': language,
        'timestamp': int(time.time()),
    }

    # Imzo yaratish
    signature = generate_signature(payload, secret_key=HMAC_SECRET_KEY)
    print("Yasalgan Signature (before quote):", signature)

    headers = {
        "X-Signature": signature,  # X-Signature to'g'ri yuborilsin
        "Content-Type": "application/json"
    }

    # Yuborilayotgan request haqida print qilish
    print("\nYuborilayotgan HEADERS:")
    for k, v in headers.items():
        print(f"{k}: {v}")
    print("\nYuborilayotgan PAYLOAD:")
    print(payload)

    async with session.post(url, json=payload, headers=headers) as response:
        print("\n===== RESPONSE INFO =====")
        print("Status Code:", response.status)
        print("Headers:", response.headers)
        response_text = await response.text()
        print("Body:", response_text)

        if response.status == 201:
            return "User created successfully"
        return f"Failed to create user: {response.status} - {response_text}"


async def check_phone_number(phone_number: str):
    url = f"{BASE_URL}/account/users/check-phone/"
    payload = {
        'phone_number': phone_number,
        'timestamp': int(time.time()),
    }
    signature = generate_signature(payload, secret_key=HMAC_SECRET_KEY)
    headers = {
        "X-Signature": signature,
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("exists", False)
            return False


async def get_user(telegram_id: int, session: aiohttp.ClientSession):
    url = f"{BASE_URL}/account/users/{telegram_id}/"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        return None


async def check_link_exist(telegram_link: str):
    url = f"{BASE_URL}/shop/shops/check-link/"
    payload = {
        'telegram_link': telegram_link,
        'timestamp': int(time.time()),
    }
    signature = generate_signature(payload, secret_key=HMAC_SECRET_KEY)
    headers = {
        "X-Signature": signature,
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("exists", False)
            return False


async def update_language_phone(telegram_id: int, language: str, phone_number: str, session: aiohttp.ClientSession):
    url = f"{BASE_URL}/account/users/update_phone/"
    payload = {
            "telegram_id": telegram_id,
            "language": language,
            "phone_number": phone_number,
            "timestamp": int(time.time()),
               }
    signature = generate_signature(payload, secret_key=HMAC_SECRET_KEY)
    headers = {
        "X-Signature": signature,
        "Content-Type": "application/json"
    }
    async with session.post(url, json=payload, headers=headers) as response:
        response_text = await response.text()
        if response.status == 201:
            return "User created successfully"
        return f"Failed to create user: {response.status} - {response_text}"


async def update_telegram_link(telegram_id: int, telegram_link: str, session: aiohttp.ClientSession):
    url = f"{BASE_URL}/account/users/update_link/"
    payload = {
            "telegram_id": telegram_id,
            "telegram_link": telegram_link,
            "timestamp": int(time.time()),
               }
    signature = generate_signature(payload, secret_key=HMAC_SECRET_KEY)
    headers = {
        "X-Signature": signature,
        "Content-Type": "application/json"
    }
    async with session.post(url, json=payload, headers=headers) as response:
        response_text = await response.text()
        if response.status == 201:
            return "User created successfully"
        return f"Failed to create user: {response.status} - {response_text}"


async def create_shop(telegram_id: int, title: str, desc: str, image: str, telegram_link: str, language: str, session: aiohttp.ClientSession):
    url = f"{BASE_URL}/shop/shops/shop-add/"
    title_field = f'title_{language}'
    desc_field = f'desc_{language}'

    payload = {
        'telegram_id': telegram_id,
        title_field: title,
        desc_field: desc,
        'image': image,
        'telegram_link': telegram_link,
        'language': language,
        'timestamp': int(time.time()),
    }
    signature = generate_signature(payload, secret_key=HMAC_SECRET_KEY)

    headers = {
        "X-Signature": signature,
        "Content-Type": "application/json"
    }

    async with session.post(url, json=payload, headers=headers) as response:
        response_text = await response.text()

        if response.status == 201:
            return "User created successfully"
        return f"Failed to create user: {response.status} - {response_text}"