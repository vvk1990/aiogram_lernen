from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Погнали!)')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='/help')
b2 = KeyboardButton(text='/vote')
kb.add(b1, b2)

ikb = InlineKeyboardMarkup(row_width=2)
inb1 = InlineKeyboardButton(text='❤️',
                            callback_data='like')
inb2 = InlineKeyboardButton(text='️👎',
                            callback_data='dislike')
ikb.add(inb1, inb2)

@dp.message_handler(commands=['start'])
async def start_command(messge: types.Message):
    await bot.send_message(chat_id=messge.from_user.id,
                           text='Welcome to our bot!',
                           reply_markup=kb)

@dp.message_handler(commands=['vote'])
async def vote_command(messge: types.Message):
    await bot.send_photo(chat_id=messge.from_user.id,
                         photo='https://upload.wikimedia.org/wikipedia/ru/thumb/1/11/The_Lost_City_%282022%29.jpg/800px-The_Lost_City_%282022%29.jpg',
                         caption='Нравится ли тебе данная фотография?',
                         reply_markup=ikb)

@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer(text='Тебе понравилась эта фотография')
    await callback.answer(text='Тебе не понравилась эиа фотография')

executor.start_polling(skip_updates=True,
                       dispatcher=dp,
                       on_startup=on_startup)