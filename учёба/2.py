# отвечаем рандомным символом алфавита и добавляем команду /description(описание бота)

from aiogram import Bot, Dispatcher, executor, types
import random

# бот - сервер который будет взаимодействовать с API telegram

TOKEN_API = '6090873017:AAGAKCPKT3mDlaUDIXC8ocetWpQc7UYBzUs' #- токен бота

HELP_COMMAND = ''' 
/help - сыписок команд
/start - начать работу с ботом
/description - описание бота
/count - показывает число вызывов этой функции
/nul - выводит yes или no
'''
aphovit = 'qwertyuiopasdfghjklzxcvbnm'

bot = Bot(TOKEN_API) # создали бота
dp = Dispatcher(bot) # создали диспетчера

# создадим переменную для подсчетов количества вызовов функции
count = 0

# создаем обработчик сообщения /count
# если есть в тексте 0 ответ да ...
# @dp.message_handler()
# async def yes_no(message: types.Message):
#     if '0' in message.text:
#         await message.answer('yes')
#     else:
#         await message.answer('no')

# создаем обработчик сообщения /count
@dp.message_handler(commands=['count'])
async def help_command(message: types.Message):
    global count
    await message.answer(f'count = {count}')
    count += 1

# создаем обработчик сообщения /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.delete()# удалим наше сообщение
    await message.answer(HELP_COMMAND)

# создаем обработчик сообщения /start
@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.reply('Приветствую вас')
    await message.delete()

# создаем обработчик сообщения /description
@dp.message_handler(commands=['description'])
async def help_command(message: types.Message):
    await message.reply('принимаем заявки')
    await message.delete()


# создаем обработчик сообщения /description
@dp.message_handler(commands=['description'])
async def help_command(message: types.Message):
    await message.reply('принимаем заявки')
    await message.delete()


# создаем обработчик наших сообщений c рандомным ответом
@dp.message_handler()
async def raandom(message: types.Message):
    await message.answer(text=random.choice(aphovit))


executor.start_polling(dp)