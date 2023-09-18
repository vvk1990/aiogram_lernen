from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from config import TOKEN_API

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

ADMIN = 1914231330

def set_key(key: str = None):
    def decorator(func):
        setattr(func, 'key', key)

        return func
    return decorator

class AdminMiddleware(BaseMiddleware):
   async def on_process_message(self, message, data):
        handler = current_handler.get()

        if handler:
            key = getattr(handler, 'key', 'Такого атрибута нет')
            print(key)


# # ставим ограничения на писанину в чате: если твой id не как нам надо тогда дальше не проходим
# class CustomMiddleware(BaseMiddleware):
#     async def on_process_message(self, message, data):
#         if message.from_user.id != ADMIN:
#             print(message.from_user.id)
#             raise CancelHandler()

@dp.message_handler(commands=['start']) # обработчик событий message
async def cdm_start(message: types.Message):
    await message.answer('Привет ты нажал на кнопку старт')

@dp.message_handler(lambda message: message.text.lower() == 'привет')
@set_key('hallo! ')
async def text_hello(message: types.Message):
    await message.reply('И тебе привет')



dp.middleware.setup(AdminMiddleware())
executor.start_polling(dp, skip_updates=True)