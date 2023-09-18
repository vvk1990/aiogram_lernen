from aiogram import Bot, Dispatcher, executor, types
# бот - сервер который будет взаимодействовать с API telegram

TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

# создаем обработчик наших сообщений
@dp.message_handler()
async def echo(message: types.Message):
    if message.text.count(' ') >= 1:# если сообщение из двцх и более слов тогда мы на него ответим
        await message.answer(text=message.text)  # ответить на сообщение
    # await message.answer(text=message.text.upper()) # ответить на сообщение эхом в верх.регистре

if __name__ == '__main__':
    executor.start_polling(dp)