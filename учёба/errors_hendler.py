import asyncio

from aiogram import executor, Bot, Dispatcher, types
from aiogram.utils.exceptions import BotBlocked
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await asyncio.sleep(10)
    await message.answer('ha')

@dp.errors_handlers(exception=BotBlocked)
async def error_bot_blocked_hendler(update: types.Update, exception: BotBlocked):
    print('нельзя отравить сообщение')

    return True

executor.start_polling(dp, skip_updates=True)