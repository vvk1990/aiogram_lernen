from aiogram import Bot, Dispatcher, executor, types
# бот - сервер который будет взаимодействовать с API telegram

TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота

HELP_COMMAND = ''' 
/help - сыписок команд
/start - начать работу с ботом
'''

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

# создаем обработчик сообщения /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(HELP_COMMAND)

# создаем обработчик сообщения /start
@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.reply('Приветствую вас')
    await message.delete()

executor.start_polling(dp)

