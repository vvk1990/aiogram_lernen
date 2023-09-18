from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота
import random
from config import TOKEN_API

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера



ikb = InlineKeyboardMarkup(row_width=2)
bat1 = InlineKeyboardButton(text='Button 1',
                            url='https://www.youtube.com/watch?v=qivjEiONPy4'
                            )
bat2 = InlineKeyboardButton(text='Button 2',
                            url='https://www.youtube.com/watch?v=qivjEiONPy4')

ikb.add(bat1, bat2)
@dp.message_handler(commands=['start'])
async def start_command(massage: types.Message):
    await bot.send_message(chat_id=massage.chat.id,
                           text='Добро пожаловать',
                           reply_markup=ikb)

async def on_startup(_):
    print('Погнали!)')


executor.start_polling(dp, on_startup=on_startup)