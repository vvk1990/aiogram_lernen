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
# 3
    async def on_process_message(self, message, data):
        print(data, message)
# 2
#     async def on_process_update(self, update, data):
#         print('hello2')
# 1
    async def on_pre_process_update(self, update: types.Update, data: dict):
        print('hello1')

@dp.message_handler(commands=['start']) # обработчик событий message
async def cdm_start(message: types.Message):
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('test', callback_data='data')]])

    await message.answer('Привет ты написал старт')
    print('world')

dp.middleware.setup(TestMiddleware()) # - регистрируем  middleware
executor.start_polling(dp, skip_updates=True)