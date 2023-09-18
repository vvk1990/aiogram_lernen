from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from config import TOKEN_API

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

ADMIN = 1914231330


class CheckMiddleware(BaseMiddleware):
   async def on_process_callback_query (self, callback: types.CallbackQuery, data):
       callback_id = callback.data[callback.data.find('_')+1:]

       if callback_id != str(callback.from_user.id):
           raise CancelHandler()

@dp.message_handler(commands=['start']) # обработчик событий message
async def cdm_start(message: types.Message):
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Тестовоя кнопка', callback_data=f'check_{message.from_user.id}' )]
    ])
    await message.answer('Тестовое сообщение', reply_markup=ikb)


@dp.callback_query_handler(lambda callback: callback.data.startswitch('check_'))
async def cb_check(callback):
    await callback.message.answer('Ты нажал на кнопку')


dp.middleware.setup(CheckMiddleware())
executor.start_polling(dp, skip_updates=True)