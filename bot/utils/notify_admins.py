from loader import bot
from data.config import ADMINS


async def start_answer():
    for i in ADMINS:
        try:
            await bot.send_message(chat_id=i, text="Bot faollashdi!")
        except:
            pass


async def shutdown_answer():
    for i in ADMINS:
        try:
            await bot.send_message(chat_id=i, text="Bot to'xtadi!")
        except:
            pass