from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from config import TOKEN_API

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

ADMIN = 191423133#0
# ставим ограничения на писанину в чате: если твой id не как нам надо тогда дальше не проходим
class CustomMiddleware(BaseMiddleware):
    async def on_process_message(self, message, data):
        if message.from_user.id != ADMIN:
            print(message.from_user.id)
            raise CancelHandler()

@dp.message_handler(commands=['start']) # обработчик событий message
async def cdm_start(message: types.Message):
    await message.answer('Привет ты нажал на кнопку старт')

@dp.message_handler(lambda message: message.text.lower() == 'привет')
async def text_hello(message: types.Message):
    await message.reply('И тебе привет')



dp.middleware.setup(CustomMiddleware())
executor.start_polling(dp, skip_updates=True)