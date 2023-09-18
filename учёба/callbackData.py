from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Погнали!)')

cb = CallbackData('ikb', 'action')

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Button', callback_data=cb.new('push'))]
])

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome to our bot!',
                           reply_markup=ikb
                           )

@dp.callback_query_handler(cb.filter())
async def ikb_cd_handler(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'push':
        await callback.answer('yps')

executor.start_polling(skip_updates=True,
                       dispatcher=dp,
                       on_startup=on_startup)