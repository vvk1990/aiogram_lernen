from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.middlewares import BaseMiddleware
# слои обработки _________
# pre_process update
# process update
# pre_process message
# filter
# process message
# handler
# post process message
# post process update


from config import TOKEN_API

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

# создали middleware который обрабатывает действие пользователя до того как он попадет а hendler
class TestMiddleware(BaseMiddleware):

    async def on_process_update(self, update, data):
        print('hello2')

    async def on_pre_process_update(self, update: types.Update, data: dict):
        print('hello')

@dp.message_handler(commands=['start'])
async def cdm_start(message: types.Message):
    await message.answer('Привет ты написал старт')
    print('world')

dp.middleware.setup(TestMiddleware()) # - запускаем middleware
executor.start_polling(dp, skip_updates=True
                          )